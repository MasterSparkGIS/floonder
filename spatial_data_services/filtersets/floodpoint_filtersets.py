import django_filters


class FloodPointFilterset(django_filters.FilterSet):
    kelurahan = django_filters.CharFilter(field_name='namobj', lookup_expr='iexact')
    kecamatan = django_filters.CharFilter(field_name='wadmkc', lookup_expr='iexact')
    kota = django_filters.CharFilter(field_name='wadmkk', lookup_expr='iexact')
    provinsi = django_filters.CharFilter(field_name='wadmpr', lookup_expr='icontains')
    month = django_filters.CharFilter(field_name='month', lookup_expr='iexact')
    year = django_filters.NumberFilter(field_name='year', lookup_expr='iexact')

