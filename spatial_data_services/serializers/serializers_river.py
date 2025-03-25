from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import River

class RiverSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = River
        geo_field = "geom"
        fields = (
            "id",
            "namobj",
            "tipsng",
            "klssng",
            "fcode",
            "remark",
            "srs_id",
            "lcode",
            "metadata",
            "namws",
            "namda",
            "status",
            "wmax",
            "dbtmax",
            "slprt",
            "shape_leng",
        )
