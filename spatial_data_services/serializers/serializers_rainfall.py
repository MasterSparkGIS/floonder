from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import Rainfall

class RainfallSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Rainfall
        geo_field = "geometry"
        fields = (
            "id",
            "fid",
            "shape_length",
            "shape_area",
            "gridcode",
        )
