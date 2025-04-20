from django.contrib.gis.db import models


class Rainfall(models.Model):
    fid = models.IntegerField(null=True, blank=True)

    shape_length = models.FloatField(null=True, blank=True)
    shape_area = models.FloatField(null=True, blank=True)
    gridcode = models.IntegerField(null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)

    geometry = models.PolygonField(srid=4326)

    def __str__(self):
        return f"Feature {self.fid or self.pk}"