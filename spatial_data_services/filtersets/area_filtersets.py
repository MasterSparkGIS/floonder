import django_filters
from ..models_floodarea import FloodArea

import django_filters
from .models_flood_area import FloodArea
from .models import AdministrationRegion # Pastikan import model AdministrationRegion

class FloodAreaFilterSet(django_filters.FilterSet):
    # Filter standar
    desa = django_filters.CharFilter(lookup_expr='icontains')
    kecamatan = django_filters.CharFilter(lookup_expr='icontains')
    bulan = django_filters.CharFilter(lookup_expr='iexact')
    tahun = django_filters.NumberFilter()
    risk_class = django_filters.NumberFilter()

    kota = django_filters.CharFilter(method='filter_by_kota')

    class Meta:
        model = FloodArea
        fields = ['desa', 'kecamatan', 'bulan', 'tahun', 'risk_class', 'kota']

    def filter_by_kota(self, queryset, name, value):
        if not value:
            return queryset

        kecamatan_list = AdministrationRegion.objects.filter(
            wadmkk__icontains=value
        ).values_list('wadmkc', flat=True).distinct()

        return queryset.filter(kecamatan__in=kecamatan_list)