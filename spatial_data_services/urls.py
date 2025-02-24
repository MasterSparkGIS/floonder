from django.urls import path

from .views import AdministrationRegionViewSet

urlpatterns = [
    path('/curah-hujan', AdministrationRegionViewSet.as_view({'get': 'list'})),
]