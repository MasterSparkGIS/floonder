from django.contrib.gis.db import models


class FloodArea(models.Model):
    desa = models.CharField(max_length=80)
    kecamatan = models.CharField(max_length=80)

    area_ha = models.FloatField()
    bulan = models.CharField(max_length=80)
    tahun = models.BigIntegerField()

    pct_very_l = models.FloatField(verbose_name="Percent Very Low")
    pct_low = models.FloatField(verbose_name="Percent Low")
    pct_medium = models.FloatField(verbose_name="Percent Medium")
    pct_high = models.FloatField(verbose_name="Percent High")
    pct_very_h = models.FloatField(verbose_name="Percent Very High")
    pct_extrem = models.FloatField(verbose_name="Percent Extreme")

    risk_score = models.FloatField()
    risk_max = models.FloatField()
    severity = models.CharField(max_length=80)
    risk_class = models.BigIntegerField()
    high_risk = models.FloatField(verbose_name="High Risk Area", db_column='high_risk_')
    extreme_ar = models.FloatField(verbose_name="Extreme Area")

    p_rainfall = models.FloatField()
    p_elevatio = models.FloatField(verbose_name="p_elevation")
    p_twi = models.FloatField()
    p_slope = models.FloatField()
    p_landuse = models.FloatField()
    p_prox = models.FloatField()

    c_rainfall = models.FloatField()
    c_elevatio = models.FloatField(verbose_name="c_elevation")
    c_twi = models.FloatField()
    c_slope = models.FloatField()
    c_landuse = models.FloatField()
    c_prox = models.FloatField()

    reason = models.CharField(max_length=165)

    geom = models.MultiPolygonField(srid=3857)

    def __str__(self):
        return f"{self.desa} - {self.kecamatan} ({self.bulan} {self.tahun})"

    class Meta:
        verbose_name = "Flood Area"
        verbose_name_plural = "Flood Areas"
