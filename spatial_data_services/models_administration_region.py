from django.contrib.gis.db import models

class AdministrationRegion(models.Model):
    kdppum = models.CharField(max_length=50, blank=True, null=True)
    namobj = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    kdpbps = models.CharField(max_length=50, blank=True, null=True)
    fcode = models.CharField(max_length=50, blank=True, null=True)
    luaswh = models.CharField(max_length=50, blank=True, null=True)
    uupp   = models.CharField(max_length=50, blank=True, null=True)
    srs_id = models.CharField(max_length=50, blank=True, null=True)
    metadata = models.CharField(max_length=255, blank=True, null=True)
    kdepum = models.CharField(max_length=50, blank=True, null=True)
    kdcbum = models.CharField(max_length=50, blank=True, null=True)
    kdbbps = models.CharField(max_length=50, blank=True, null=True)
    wadmkc = models.CharField(max_length=100, blank=True, null=True)
    wadmkd = models.CharField(max_length=100, blank=True, null=True)
    wadmkk = models.CharField(max_length=100, blank=True, null=True)
    wadmpr = models.CharField(max_length=100, blank=True, null=True)
    tipadm = models.CharField(max_length=50, blank=True, null=True)

    shape_leng = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)

    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

    def __str__(self):
        return self.namobj if self.namobj else "Wilayah Administrasi (ID: {})".format(self.id)
