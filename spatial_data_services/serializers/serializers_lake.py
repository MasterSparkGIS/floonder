from rest_framework_gis import serializers

from ..models import Lake

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