import geopandas as gpd
from rasterstats import zonal_stats
import rasterio
from rasterio.mask import mask
from shapely.geometry import Point, mapping
import numpy as np
import pandas as pd
import sys

target_crs = "EPSG:4326"

gdf_admin = gpd.read_file("data/ADMINISTRASIDESA_AR_25K.shp").to_crs(target_crs)
gdf_admin_bandung_barat = gpd.read_file("data/bandung-barat/ADMINISTRASIDESA_AR_25K.shp").to_crs(target_crs)
gdf_admin_kab_bandung = gpd.read_file("data/kab-bandung/ADMINISTRASIDESA_AR_25K.shp").to_crs(target_crs)
gdf_admin_cimahi = gpd.read_file("data/KOTACIMAHI/ADMINISTRASIDESA_AR_25K.shp").to_crs(target_crs)

gdf_admin_all = gpd.GeoDataFrame(
    pd.concat([gdf_admin, gdf_admin_bandung_barat, gdf_admin_kab_bandung, gdf_admin_cimahi], ignore_index=True),
    crs=target_crs
)

month = sys.argv[1]

gdf_rain = gpd.read_file(f"data/curah-hujan-{month}.geojson").to_crs(target_crs)
gdf_admin_rain = gpd.overlay(gdf_admin_all, gdf_rain, how='intersection')

dem_path = "data/dem-merged.tif"
stats_dem = zonal_stats(
    gdf_admin_rain,
    dem_path,
    stats=["min", "max", "mean", "std"],
    geojson_out=True
)
gdf_stats_dem = gpd.GeoDataFrame.from_features(stats_dem, crs=target_crs)
gdf_admin_rain["dem_min"] = gdf_stats_dem["min"]
gdf_admin_rain["dem_max"] = gdf_stats_dem["max"]
gdf_admin_rain["dem_mean"] = gdf_stats_dem["mean"]
gdf_admin_rain["dem_std"] = gdf_stats_dem["std"]

slope_path = "data/reprojected-slope.tif"
stats_slope = zonal_stats(
    gdf_admin_rain,
    slope_path,
    stats=["mean"],
    geojson_out=True
)
gdf_stats_slope = gpd.GeoDataFrame.from_features(stats_slope, crs=target_crs)
gdf_admin_rain["avg_slope"] = gdf_stats_slope["mean"]

threshold_dict = {}
for adm, group in gdf_admin_rain.groupby("WADMKK"):
    avg = group["dem_mean"].mean()
    std = group["dem_std"].mean()
    threshold_dict[adm] = avg - 0.5 * std

def enhanced_flood_potential(row):
    """
    Menghitung skor risiko gabungan dari:
      - Nilai hujan (gridcode)
      - Elevasi (dem_mean dibandingkan threshold)
      - Kemiringan lereng (avg_slope)

    Titik dianggap berpotensi banjir bila composite score > 0.5.
    """
    grid_val = row.get("gridcode", 0)
    if grid_val < 2:
        return False

    grid_risk = (grid_val - 1) / 8

    threshold = threshold_dict.get(row["WADMKK"], row["dem_mean"])
    elev_diff = threshold - row["dem_mean"]
    elev_risk = 1 / (1 + np.exp(-elev_diff / 2)) if threshold > 0 else 0

    slope = row.get("avg_slope", 20)
    slope_risk = 1 - min(slope / 20, 1)

    composite_score = (0.4 * grid_risk) + (0.4 * elev_risk) + (0.2 * slope_risk)

    return composite_score > 0.5

gdf_admin_rain["potensi_banjir"] = gdf_admin_rain.apply(enhanced_flood_potential, axis=1)

gdf_sungai_1 = gpd.read_file("data/KOTABANDUNG/SUNGAI_LN_25K.shp")
gdf_sungai_1.crs = target_crs
gdf_sungai_2 = gpd.read_file("data/kab-bandung/SUNGAI_LN_25K.shp")
gdf_sungai_2.crs = target_crs
gdf_sungai_3 = gpd.read_file("data/bandung-barat/SUNGAI_LN_25K.shp")
gdf_sungai_3.crs = target_crs

gdf_sungai = gpd.GeoDataFrame(
    pd.concat([gdf_sungai_1, gdf_sungai_2, gdf_sungai_3], ignore_index=True),
    crs=target_crs
)

gdf_danau_1 = gpd.read_file("data/KOTABANDUNG/DANAU_AR_25K.shp")
gdf_danau_1.crs = target_crs
gdf_danau_2 = gpd.read_file("data/kab-bandung/DANAU_AR_25K.shp")
gdf_danau_2.crs = target_crs
gdf_danau_3 = gpd.read_file("data/bandung-barat/DANAU_AR_25K.shp")
gdf_danau_3.crs = target_crs

gdf_danau = gpd.GeoDataFrame(
    pd.concat([gdf_danau_1, gdf_danau_2, gdf_danau_3], ignore_index=True),
    crs=target_crs
)

gdf_admin_rain_3857 = gdf_admin_rain.to_crs("EPSG:3857")
gdf_sungai_3857 = gdf_sungai.to_crs("EPSG:3857")

gdf_admin_rain_3857["dist_to_river"] = gdf_admin_rain_3857.centroid.apply(
    lambda x: gdf_sungai_3857.distance(x).min()
)
gdf_admin_rain["dist_to_river"] = gdf_admin_rain_3857["dist_to_river"]

print("BREAKPOINT")

titik_list = []
with rasterio.open(dem_path) as src_dem, rasterio.open(slope_path) as src_slope:
    for idx, row in gdf_admin_rain[gdf_admin_rain["potensi_banjir"]].iterrows():
        geom = [mapping(row.geometry)]
        try:
            out_image_dem, out_transform_dem = mask(src_dem, geom, crop=True)
            out_image_slope, out_transform_slope = mask(src_slope, geom, crop=True)
        except Exception as e:
            print(f"Error masking polygon idx {idx}: {e}")
            continue

        data_dem = out_image_dem[0].astype(float)
        data_slope = out_image_slope[0].astype(float)

        if src_dem.nodata is not None:
            data_dem[data_dem == src_dem.nodata] = np.nan
        if src_slope.nodata is not None:
            data_slope[data_slope == src_slope.nodata] = np.nan

        if np.all(np.isnan(data_dem)):
            continue

        min_index = np.unravel_index(np.nanargmin(data_dem), data_dem.shape)
        flood_elev = float(np.nanmin(data_dem))
        x, y = rasterio.transform.xy(out_transform_dem, min_index[0], min_index[1])
        titik_banjir = Point(x, y)

        avg_slope = np.nanmean(data_slope)

        titik_banjir_3857 = gpd.GeoSeries([titik_banjir], crs=target_crs).to_crs("EPSG:3857").geometry[0]
        dist_to_river = gdf_sungai_3857.distance(titik_banjir_3857).min()

        if dist_to_river <= 20:
            continue

        gdf_danau_3857 = gdf_danau.to_crs("EPSG:3857")
        if gdf_danau_3857.buffer(30).contains(titik_banjir_3857).any():
            continue

        idx_nearest = gdf_sungai_3857.distance(titik_banjir_3857).idxmin()
        nearest_river = gdf_sungai_3857.loc[idx_nearest].geometry

        river_buffer_3857 = nearest_river.buffer(10)
        river_buffer = gpd.GeoSeries([river_buffer_3857], crs="EPSG:3857").to_crs(target_crs).geometry[0]
        river_stats = zonal_stats([river_buffer], dem_path, stats=["mean"])[0]
        river_elev = river_stats["mean"] if river_stats["mean"] is not None else np.nan

        if np.isnan(river_elev):
            continue

        titik_atribut = row.copy()
        titik_atribut["geometry"] = titik_banjir
        titik_atribut["flood_elev"] = flood_elev
        titik_atribut["river_elev"] = river_elev
        titik_atribut["dist_to_river"] = dist_to_river
        titik_atribut["avg_slope"] = avg_slope
        titik_atribut["year"] = 2025
        titik_list.append(titik_atribut)

gdf_titik_banjir = gpd.GeoDataFrame(titik_list, crs=target_crs)

def calculate_risk_score(row):
    score = 0

    gridcode_weights = {
        1: 0,
        2: 1,
        3: 3,
        4: 5,
        5: 7,
        6: 9,
        7: 11,
        8: 13,
        9: 15
    }
    grid_val = row.get("gridcode", 0)
    score += gridcode_weights.get(grid_val, 0)

    elev_diff = row["dem_mean"] - row["flood_elev"]
    if elev_diff > 10:
        score += 10
    elif elev_diff > 5:
        score += 5
    elif elev_diff > 2:
        score += 2

    diff = row["river_elev"] - row["flood_elev"]
    if diff > 10:
        score += 10
    elif diff > 5:
        score += 5
    elif diff > 2:
        score += 2
    elif diff > 0:
        score += 1
    else:
        score += 5

    if row["dist_to_river"] < 200:
        score += 10
    elif row["dist_to_river"] < 500:
        score += 5
    elif row["dist_to_river"] < 1000:
        score += 2

    if not np.isnan(row["avg_slope"]):
        if row["avg_slope"] < 3.5:
            score += 10
        elif row["avg_slope"] < 8.75:
            score += 5
        elif row["avg_slope"] < 17.5:
            score += 2

    return score

gdf_titik_banjir["risk_score"] = gdf_titik_banjir.apply(calculate_risk_score, axis=1)

def classify_risk_from_score(score):
    if score >= 50:
        return "Sangat Rawan"
    elif score >= 35:
        return "Rawan"
    elif score >= 20:
        return "Sedang"
    elif score >= 10:
        return "Rendah"
    else:
        return "Sangat Rendah"

gdf_titik_banjir["risk_level"] = gdf_titik_banjir["risk_score"].apply(classify_risk_from_score)

gdf_titik_banjir.to_file(f"hasil_titik_banjir-{month}.geojson", driver="GeoJSON")