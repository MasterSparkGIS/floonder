from django.db.models import Avg
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import AdministrationRegion, Rainfall
from ..models_dem import DigitalElevationModel
from ..utils import get_rainfall, month_dict

from datetime import datetime

class AdministrationRegionSerializer(GeoFeatureModelSerializer):
    curah_hujan = serializers.SerializerMethodField()
    desa = serializers.CharField(source="namobj")
    kecamatan = serializers.CharField(source="wadmkc")
    wilayah = serializers.CharField(source="wadmkk")
    provinsi = serializers.CharField(source="wadmpr")
    month = serializers.SerializerMethodField()

    class Meta:
        model = AdministrationRegion
        geo_field = "geom"
        fields = (
            "id",
            "kdppum",
            "desa",
            "kecamatan",
            "wilayah",
            "provinsi",
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
            "tipadm",
            "shape_leng",
            "shape_area",
            "curah_hujan",
            "month"
        )

    def get_month(self, obj):
        month = self.context.get('month')
        if not month:
            month = datetime.now().month
        return month_dict[int(month)]

    def get_curah_hujan(self, obj):
        month = self.get_month(obj)
        rain_areas = Rainfall.objects.filter(
            geometry__intersects=obj.geom,
            month=month
        )
        gridcodes = [
            get_rainfall(rain.gridcode)
            for rain in rain_areas
            if not obj.geom.intersection(rain.geometry).empty
        ]
        return gridcodes if gridcodes else None