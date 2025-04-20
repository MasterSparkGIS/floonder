
import math


def calculate_risk_score(gridcode, dem_mean, flood_elev, river_elev, dist_to_river, avg_slope):
    """Calculate flood risk score based on various parameters"""
    score = 0

    # Score based on gridcode (rainfall intensity)
    gridcode_weights = {
        1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 9, 7: 11, 8: 13, 9: 15
    }
    score += gridcode_weights.get(gridcode, 0)

    # Score based on elevation difference between mean and lowest point
    elev_diff = dem_mean - flood_elev
    if elev_diff > 10:
        score += 10
    elif elev_diff > 5:
        score += 5
    elif elev_diff > 2:
        score += 2

    # Score based on river elevation vs lowest point elevation
    if river_elev is not None:
        diff = river_elev - flood_elev
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

    # Score based on distance to river
    if dist_to_river < 200:
        score += 10
    elif dist_to_river < 500:
        score += 5
    elif dist_to_river < 1000:
        score += 2

    # Score based on slope
    if avg_slope < 3.5:
        score += 10
    elif avg_slope < 8.75:
        score += 5
    elif avg_slope < 17.5:
        score += 2

    return score


def classify_risk_level(score):
    """Classify risk level based on score"""
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


def enhanced_flood_potential(gridcode, dem_mean, dem_std, avg_slope, threshold):
    """Determine flood potential based on various parameters"""
    if gridcode < 2:
        return False

    grid_risk = (gridcode - 1) / 8

    if threshold > 0:
        elev_diff = threshold - dem_mean
        elev_risk = 1 / (1 + math.exp(-elev_diff / 2))
    else:
        elev_risk = 0

    slope_risk = 1 - min(avg_slope / 20, 1)

    composite_score = (0.4 * grid_risk) + (0.4 * elev_risk) + (0.2 * slope_risk)

    return composite_score > 0.5

def get_rainfall(gridcode):
    curah = "No Data"

    if gridcode == 1:
        curah = "0-20mm"
    elif gridcode == 2:
        curah = "20-50mm"
    elif gridcode == 3:
        curah = "50-100mm"
    elif gridcode == 4:
        curah = "100-150mm"
    elif gridcode == 5:
        curah = "150-200mm"
    elif gridcode == 6:
        curah = "200-300mm"
    elif gridcode == 7:
        curah = "300-400mm"
    elif gridcode == 8:
        curah = "400-500mm"
    elif gridcode == 9:
        curah = "> 500mm"

    return curah

month_dict = {
    1 : "januari",
    2 : "februari",
    3 : "maret",
    4 : "april",
    5 : "mei",
    6 : "juni",
    7 : "juli",
    8 : "agustus",
    9 : "september",
    10 : "oktober",
    11 : "november",
    12 : "desember",
}