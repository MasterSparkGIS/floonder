from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from ..models import AdministrationRegion, Rainfall

class RainfallSerializer(ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = Rainfall
        geo_field = None
        fields = ('fid', 'gridcode', 'label')


    def get_label(self, obj):
        rainfall_mapping = {
            1: '0-20 mm',
            2: '21-50 mm',
            3: '51-100 mm',
            4: '101-200 mm',
            5: '201-300 mm',
            6: '301-400 mm',
            7: '401-500 mm',
            8: '501-600 mm',
            9: '>500 mm'
        }

        return rainfall_mapping.get(obj.gridcode, f"Gridcode {obj.gridcode}")

class AdministrationRegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AdministrationRegion
        geo_field = 'geometry'
        fields = ('id', 'namobj')

    def get_properties(self, instance, fields):
        properties = super().get_properties(instance, fields)
        properties['name'] = instance.namobj
        rainfalls = self.get_rainfalls(instance)
        if rainfalls:
            properties['fid'] = rainfalls[0]['fid']
            properties['gridcode'] = rainfalls[0]['gridcode']
            properties['rainfall_label'] = rainfalls[0]['label']
        return properties

    def get_rainfalls(self, obj):
        qs = Rainfall.objects.filter(geometry__intersects=obj.geometry)
        return RainfallSerializer(qs, many=True).data