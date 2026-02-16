import django_filters
from ..models_floodarea import FloodArea


MONTH_NAME_TO_INT = {
    'januari': 1, 'februari': 2, 'maret': 3, 'april': 4,
    'mei': 5, 'juni': 6, 'juli': 7, 'agustus': 8,
    'september': 9, 'oktober': 10, 'november': 11, 'desember': 12,
    'january': 1, 'february': 2, 'march': 3, 'may': 5,
    'june': 6, 'july': 7, 'august': 8, 'october': 10,
    'december': 12,
}


class FloodAreaFilterSet(django_filters.FilterSet):
    bulan = django_filters.CharFilter(method='filter_by_bulan')
    tahun = django_filters.NumberFilter(field_name='year')
    kota = django_filters.CharFilter(field_name='WADMKK', lookup_expr='icontains')
    kecamatan = django_filters.CharFilter(field_name='WADMKC', lookup_expr='icontains')
    desa = django_filters.CharFilter(field_name='WADMKD', lookup_expr='icontains')
    severity = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = FloodArea
        fields = ['bulan', 'tahun', 'kota', 'kecamatan', 'desa', 'severity']

    def filter_by_bulan(self, queryset, name, value):
        if not value:
            return queryset
        month_int = MONTH_NAME_TO_INT.get(value.lower())
        if month_int is not None:
            return queryset.filter(month=month_int)
        try:
            return queryset.filter(month=int(value))
        except (ValueError, TypeError):
            return queryset.none()