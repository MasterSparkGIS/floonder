from django.contrib.gis.db import models


class FloodArea(models.Model):
    # Field String (Length 80)
    desa = models.CharField(max_length=80, null=True)
    kecamatan = models.CharField(max_length=80, null=True)

    # Field Real (Precision 15)
    area_ha = models.FloatField()

    # Field String & Integer
    bulan = models.CharField(max_length=80)
    tahun = models.BigIntegerField()  # Integer64

    # Percentages (Real)
    pct_very_l = models.FloatField(verbose_name="Percent Very Low")
    pct_low = models.FloatField(verbose_name="Percent Low")
    pct_medium = models.FloatField(verbose_name="Percent Medium")
    pct_high = models.FloatField(verbose_name="Percent High")
    pct_very_h = models.FloatField(verbose_name="Percent Very High")
    pct_extrem = models.FloatField(verbose_name="Percent Extreme")

    # Risk Metrics (Real)
    risk_score = models.FloatField()
    risk_max = models.FloatField()

    # Perhatikan nama field dengan underscore di akhir sesuai tabel
    high_risk = models.FloatField(verbose_name="High Risk Area", db_column="high_risk_", null=True)
    extreme_ar = models.FloatField(verbose_name="Extreme Area")
    composite = models.FloatField(verbose_name="Composite", db_column="composite_", null=True)  # Field Baru

    # Class & Severity
    severity = models.CharField(max_length=80)
    risk_class = models.BigIntegerField()  # Integer64

    # P_ Variables (Physical?) - Real
    p_rainfall = models.FloatField()
    p_elevatio = models.FloatField(verbose_name="p_elevation")  # Sesuai tabel (terpotong)
    p_twi = models.FloatField()
    p_slope = models.FloatField()
    p_landuse = models.FloatField()
    p_prox = models.FloatField()

    # C_ Variables (Climate?) - Real
    c_rainfall = models.FloatField()
    c_elevatio = models.FloatField(verbose_name="c_elevation")  # Sesuai tabel (terpotong)
    c_twi = models.FloatField()
    c_slope = models.FloatField()
    c_landuse = models.FloatField()
    c_prox = models.FloatField()

    # Reason (Updated Length to 231)
    reason = models.CharField(max_length=231)

    # Field Baru sesuai Tabel
    dominant_f = models.CharField(max_length=80, null=True, verbose_name="Dominant Factor")
    confidence = models.FloatField(null=True)
    certainty = models.FloatField(null=True, verbose_name="Certainty")

    # Geometry (Wajib untuk GIS models, meskipun tidak ada di list atribut tabel)
    geom = models.MultiPolygonField(srid=3857)

    def __str__(self):
        return f"{self.desa} - {self.kecamatan} ({self.bulan} {self.tahun})"

    class Meta:
        verbose_name = "Flood Area"
        verbose_name_plural = "Flood Areas"
        # Jika tabel ini sudah ada di database (legacy), Anda mungkin perlu:
        # db_table = 'nama_tabel_di_db'
        # managed = False