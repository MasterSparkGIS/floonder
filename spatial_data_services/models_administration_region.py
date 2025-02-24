from django.contrib.gis.db import models

class AdministrationRegion(models.Model):
    kdppum    = models.CharField(max_length=50, null=True, blank=True)
    namobj    = models.CharField(max_length=255, null=True, blank=True)
    remark    = models.CharField(max_length=255, null=True, blank=True)
    kdpbps    = models.CharField(max_length=50, null=True, blank=True)
    fcode     = models.CharField(max_length=50, null=True, blank=True)
    luaswh    = models.FloatField(null=True, blank=True)
    uupp      = models.CharField(max_length=50, null=True, blank=True)
    srs_id    = models.CharField(max_length=50, null=True, blank=True)
    lcode     = models.CharField(max_length=50, null=True, blank=True)
    metadata  = models.TextField(null=True, blank=True)
    kdebps    = models.CharField(max_length=50, null=True, blank=True)
    kdepum    = models.CharField(max_length=50, null=True, blank=True)
    kdcbps    = models.CharField(max_length=50, null=True, blank=True)
    kdcpum    = models.CharField(max_length=50, null=True, blank=True)
    kdbbps    = models.CharField(max_length=50, null=True, blank=True)
    kdbpum    = models.CharField(max_length=50, null=True, blank=True)
    wadmkd    = models.CharField(max_length=100, null=True, blank=True)
    wiadkd    = models.CharField(max_length=100, null=True, blank=True)
    wadmkc    = models.CharField(max_length=100, null=True, blank=True)
    wiadkc    = models.CharField(max_length=100, null=True, blank=True)
    wadmkk    = models.CharField(max_length=100, null=True, blank=True)
    wiadkk    = models.CharField(max_length=100, null=True, blank=True)
    wadmpr    = models.CharField(max_length=100, null=True, blank=True)
    wiadpr    = models.CharField(max_length=100, null=True, blank=True)
    tipadm    = models.IntegerField(null=True, blank=True)
    shape_leng = models.FloatField(null=True, blank=True)
    shape_area = models.FloatField(null=True, blank=True)

    geometry = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.namobj or "Unnamed Desa Administrasi"