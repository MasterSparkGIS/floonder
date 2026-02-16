from django.contrib.gis.db import models


class FloodArea(models.Model):
    # Area & Risk Metrics
    area_ha = models.FloatField(null=True, blank=True, verbose_name="Area (Hectares)")
    pixel_coun = models.BigIntegerField(null=True, blank=True, verbose_name="Pixel Count")
    risk_score = models.FloatField(null=True, blank=True, verbose_name="Risk Score")
    risk_max = models.FloatField(null=True, blank=True, verbose_name="Risk Maximum")

    # Percentages (Real)
    pct_extrem = models.FloatField(null=True, blank=True, verbose_name="Percent Extreme")
    pct_very_h = models.FloatField(null=True, blank=True, verbose_name="Percent Very High")
    pct_high = models.FloatField(null=True, blank=True, verbose_name="Percent High")

    # Administrative Fields (dari shapefile Indonesia)
    KDPPUM = models.CharField(max_length=80, null=True, blank=True)
    NAMOBJ = models.CharField(max_length=80, null=True, blank=True, verbose_name="Nama Objek")
    REMARK = models.CharField(max_length=255, null=True, blank=True)
    KDPBPS = models.CharField(max_length=80, null=True, blank=True)
    FCODE = models.CharField(max_length=80, null=True, blank=True)
    LUASWH = models.FloatField(null=True, blank=True, verbose_name="Luas Wilayah")
    UUPP = models.CharField(max_length=80, null=True, blank=True)
    SRS_ID = models.CharField(max_length=80, null=True, blank=True)
    LCODE = models.CharField(max_length=80, null=True, blank=True)
    METADATA = models.TextField(null=True, blank=True)

    # Kode BPS dan PUM
    KDEBPS = models.CharField(max_length=80, null=True, blank=True)
    KDEPUM = models.CharField(max_length=80, null=True, blank=True)
    KDCBPS = models.CharField(max_length=80, null=True, blank=True)
    KDCPUM = models.CharField(max_length=80, null=True, blank=True)
    KDBBPS = models.CharField(max_length=80, null=True, blank=True)
    KDBPUM = models.CharField(max_length=80, null=True, blank=True)

    # Wilayah Administratif
    WADMKD = models.CharField(max_length=80, null=True, blank=True, verbose_name="Wilayah Adm Kelurahan/Desa")
    WIADKD = models.CharField(max_length=80, null=True, blank=True)
    WADMKC = models.CharField(max_length=80, null=True, blank=True, verbose_name="Wilayah Adm Kecamatan")
    WIADKC = models.CharField(max_length=80, null=True, blank=True)
    WADMKK = models.CharField(max_length=80, null=True, blank=True, verbose_name="Wilayah Adm Kabupaten/Kota")
    WIADKK = models.CharField(max_length=80, null=True, blank=True)
    WADMPR = models.CharField(max_length=80, null=True, blank=True, verbose_name="Wilayah Adm Provinsi")
    WIADPR = models.CharField(max_length=80, null=True, blank=True)

    TIPADM = models.BigIntegerField(null=True, blank=True, verbose_name="Tipe Administrasi")

    # Shape Metrics
    SHAPE_Leng = models.FloatField(null=True, blank=True, verbose_name="Shape Length")
    SHAPE_Area = models.FloatField(null=True, blank=True, verbose_name="Shape Area")

    year = models.IntegerField(null=True, blank=True, verbose_name="Year of Flood Event")
    month = models.IntegerField(null=True, blank=True, verbose_name="Month of Flood Event")

    # P_ Variables (Physical Parameters) - Real
    p_rainfall = models.FloatField(null=True, blank=True, verbose_name="Physical: Rainfall")
    p_elevatio = models.FloatField(null=True, blank=True, verbose_name="Physical: Elevation")
    p_slope = models.FloatField(null=True, blank=True, verbose_name="Physical: Slope")
    p_twi = models.FloatField(null=True, blank=True, verbose_name="Physical: TWI")
    p_landuse = models.FloatField(null=True, blank=True, verbose_name="Physical: Land Use")
    p_prox = models.FloatField(null=True, blank=True, verbose_name="Physical: Proximity")

    # C_ Variables (Contribution/Coefficient) - Real
    c_rainfall = models.FloatField(null=True, blank=True, verbose_name="Contribution: Rainfall")
    c_elev = models.FloatField(null=True, blank=True, verbose_name="Contribution: Elevation")
    c_slope = models.FloatField(null=True, blank=True, verbose_name="Contribution: Slope")
    c_twi = models.FloatField(null=True, blank=True, verbose_name="Contribution: TWI")
    c_landuse = models.FloatField(null=True, blank=True, verbose_name="Contribution: Land Use")
    c_prox = models.FloatField(null=True, blank=True, verbose_name="Contribution: Proximity")

    # Risk Classification
    composite = models.FloatField(null=True, blank=True, verbose_name="Composite Risk", db_column="composite_")
    severity = models.CharField(max_length=80, null=True, blank=True, verbose_name="Severity Level")
    reason = models.TextField(null=True, blank=True, verbose_name="Risk Reason")

    # Analysis Metrics
    dominant = models.CharField(max_length=80, null=True, blank=True, verbose_name="Dominant Factor")
    conf = models.FloatField(null=True, blank=True, verbose_name="Confidence")
    cert = models.FloatField(null=True, blank=True, verbose_name="Certainty")

    # Geometry (SRID 4326 untuk WGS84) - NOT NULL karena ini GIS model
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        kelurahan = self.WADMKD or self.NAMOBJ or "Unknown"
        kecamatan = self.WADMKC or "Unknown"
        severity = self.severity or "N/A"
        return f"{kelurahan}, {kecamatan} - {severity}"

    class Meta:
        verbose_name = "Flood Area"
        verbose_name_plural = "Flood Areas"
        db_table = 'spatial_data_services_floodarea'
        ordering = ['-risk_score']
        indexes = [
            models.Index(fields=['WADMKD', 'WADMKC']),
            models.Index(fields=['severity']),
            models.Index(fields=['risk_score']),
        ]