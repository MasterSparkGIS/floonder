from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import Rainfall
from ..utils import get_rainfall


class RainfallSerializer(GeoFeatureModelSerializer):
    curah_hujan = serializers.SerializerMethodField()

    class Meta:
        model = Rainfall
        geo_field = "geometry"
        fields = (
            "id",
            "fid",
            "shape_length",
            "shape_area",
            "curah_hujan",
            "month",
        )

        def get_curah_hujan(self, obj):
            return get_rainfall(obj.gridcode)

