from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import FloodPoint

class FloodPointSerializer(GeoFeatureModelSerializer):

    desa = serializers.CharField(source="namobj", read_only=True)
    kecamatan = serializers.CharField(source="wadmkc", read_only=True)
    wilayah = serializers.CharField(source="wadmkk", read_only=True)
    provinsi = serializers.CharField(source="wadmpr", read_only=True)

    class Meta:
        model = FloodPoint
        geo_field = "geometry"
        fields = (
            "kdppum",
            "desa",
            "remark",
            "kecamatan",
            "wilayah",
            "provinsi",
            "month",
            "year",
            "gridcode",
            "dem_min",
            "dem_max",
            "dem_mean",
            "dem_std",
            "avg_slope",
            "dist_to_river",
            "flood_elev",
            "river_elev",
            "risk_score",
            "risk_level",
        )
