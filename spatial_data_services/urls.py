from django.urls import path

from .views import AdministrationRegionViewSet, RainfallViewSet, RiverViewSet, DEMViewSet, LakeViewSet, SlopeViewSet, \
    PropertyViewSet, FloodPointViewSet, KosanViewSet

urlpatterns = [
    path('/curah-hujan', RainfallViewSet.as_view({'get': 'list'})),
    path('/wilayah-administrasi', AdministrationRegionViewSet.as_view({'get': 'list'})),
    path("/sungai", RiverViewSet.as_view({'get': 'list'})),
    path('/digital-elevation-model', DEMViewSet.as_view({'get': 'list'})),
    path('/danau', LakeViewSet.as_view({'get': 'list'})),
    path('/slope', SlopeViewSet.as_view({'get': 'list'})),
    path('/properti', PropertyViewSet.as_view({
        'get': 'list'
    })),
    path('/flood-point', FloodPointViewSet.as_view({
        'get': 'list',
    })),
    path('/kosan', KosanViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
]