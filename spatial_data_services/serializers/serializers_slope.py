from rest_framework_gis import serializers

from ..models import Slope

class SlopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slope
        fields = "__all__"