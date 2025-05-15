from django.contrib.gis.db import models

class Kosan(models.Model):
    nama = models.CharField(max_length=255, null=True, blank=True)
    alamat_lengkap = models.CharField(max_length=255, null=True, blank=True)
    luas_bangunan = models.FloatField(null=True, blank=True)
    link_lengkap_properti = models.URLField(null=True, blank=True)

    geometry = models.PointField(srid=4326)

    def __str__(self):
        return self.nama if self.nama else "Kosan tanpa nama"