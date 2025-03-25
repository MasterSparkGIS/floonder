from django.contrib.gis.db import models

class Slope(models.Model):
    name = models.CharField(max_length=255)
    raster = models.RasterField()

    def __str__(self):
        return self.name