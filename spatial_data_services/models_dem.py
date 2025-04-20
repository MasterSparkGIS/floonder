from django.contrib.gis.db import models

class DigitalElevationModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rast = models.RasterField(blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name