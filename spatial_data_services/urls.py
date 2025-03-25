from django.urls import path

from .views import AdministrationRegionViewSet, RainfallViewSet, RiverViewSet

urlpatterns = [
    path('/curah-hujan', RainfallViewSet.as_view({'get': 'list'})),
    path('/wilayah-administrasi', AdministrationRegionViewSet.as_view({'get': 'list'})),
    path("/sungai", RiverViewSet.as_view({'get': 'list'})),
]