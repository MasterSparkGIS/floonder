from rest_framework_gis import serializers

from ..models import DigitalElevationModel

class DigitalElevationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalElevationModel
        fields = "__all__"