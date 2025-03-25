from django.contrib.gis.db import models

class DigitalElevationModel(models.Model):
    layer = models.CharField(max_length=255, blank=True, null=True)
    fid = models.IntegerField(blank=True, null=True)
    attribute = models.CharField(max_length=255, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.layer} - {self.attribute} ({self.fid}): {self.value}"