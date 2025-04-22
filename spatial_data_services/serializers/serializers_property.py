from rest_framework_gis.serializers import GeoFeatureModelSerializer

from spatial_data_services.models_property import Property

from django.contrib.gis.db import models

class PropertySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Property
        geo_field = "geometry"
        fields = (
            "id",
            "nama_properti",
            "alamat_lengkap",
            "kelurahan",
            "jalan_terdekat",
            "kategori_properti",
            "status_properti",
            "harga_properti",
            "luas_bangunan",
            "luas_tanah",
            "kecamatan",
            "link_lengkap_properti",
        )