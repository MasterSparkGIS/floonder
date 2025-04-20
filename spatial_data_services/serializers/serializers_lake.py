from rest_framework_gis import serializers

from ..models import Lake
# class Lake(models.Model):
#     namobj = models.CharField(max_length=255, null=True, blank=True)
#     otodan = models.IntegerField(null=True, blank=True)
#     fcode = models.IntegerField(null=True, blank=True)
#     remark = models.CharField(max_length=255, null=True, blank=True)
#     kodlok = models.CharField(max_length=50, null=True, blank=True)
#     srs_id = models.CharField(max_length=50, null=True, blank=True)
#     lcode = models.CharField(max_length=50, null=True, blank=True)
#     metadata = models.CharField(max_length=255, null=True, blank=True)
#     voltap = models.IntegerField(null=True, blank=True)
#     dta = models.IntegerField(null=True, blank=True)
#     sedimn = models.IntegerField(null=True, blank=True)
#     vlsdn = models.IntegerField(null=True, blank=True)
#     quaar = models.IntegerField(null=True, blank=True)
#     crh = models.IntegerField(null=True, blank=True)
#     kpts = models.IntegerField(null=True, blank=True)
#     namwas = models.CharField(max_length=255, null=True, blank=True)
#     namdas = models.CharField(max_length=255, null=True, blank=True)
#     lokasi = models.CharField(max_length=255, null=True, blank=True)
#
#     shape_leng = models.FloatField(null=True, blank=True)
#     shape_area = models.FloatField(null=True, blank=True)
#
#     geom = models.MultiPolygonField(srid=4326, null=True, blank=True)
#
#     def __str__(self):
#         return self.namobj or "Danau (Unnamed)"
class LakeSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Lake
        geo_field = "geom"
        fields = (
            "id",
            "namobj",
            "otodan",
            "fcode",
            "remark",
            "kodlok",
            "srs_id",
            "lcode",
            "metadata",
            "voltap",
            "dta",
            "sedimn",
            "vlsdn",
            "quaar",
            "crh",
            "kpts",
            "namwas",
            "namdas",
            "lokasi",
            "shape_leng",
            "shape_area",
        )