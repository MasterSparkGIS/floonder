from rest_framework_gis.serializers import GeoFeatureModelSerializer

from spatial_data_services.models_floodarea import FloodArea


class FloodAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FloodArea
        geo_field = 'geom'
        fields = '__all__'