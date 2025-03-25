from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import AdministrationRegion

class AdministrationRegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AdministrationRegion
        geo_field = "geom"
        fields = (
            "id",
            "kdppum",
            "namobj",
            "remark",
            "kdpbps",
            "fcode",
            "luaswh",
            "uupp",
            "srs_id",
            "metadata",
            "kdepum",
            "kdcbum",
            "kdbbps",
            "wadmkc",
            "wadmkd",
            "wadmkk",
            "wadmpr",
            "tipadm",
            "shape_leng",
            "shape_area",
        )