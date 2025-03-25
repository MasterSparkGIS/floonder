from django.contrib.gis.db import models

class River(models.Model):
    namobj = models.CharField(max_length=255, null=True, blank=True)
    tipsng = models.IntegerField(null=True, blank=True)
    klssng = models.IntegerField(null=True, blank=True)
    fcode = models.CharField(max_length=255, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    srs_id = models.CharField(max_length=255, null=True, blank=True)
    lcode = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.CharField(max_length=255, null=True, blank=True)
    namws = models.CharField(max_length=255, null=True, blank=True)
    namda = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    wmax = models.IntegerField(null=True, blank=True)
    dbtmax = models.IntegerField(null=True, blank=True)
    slprt = models.IntegerField(null=True, blank=True)
    shape_leng = models.FloatField(null=True, blank=True)

    geom = models.MultiLineStringField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.namobj if self.namobj else "Sungai tanpa nama"
