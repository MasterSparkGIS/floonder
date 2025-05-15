from rest_framework_gis import serializers

from spatial_data_services.models_kosan import Kosan


class KosanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kosan
        fields = "__all__"
