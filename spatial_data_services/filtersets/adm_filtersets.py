import django_filters


class AdmFilterSet(django_filters.FilterSet):
    kelurahan = django_filters.CharFilter(field_name='namobj', lookup_expr='icontains')
    kecamatan = django_filters.CharFilter(field_name='wadmkc', lookup_expr='icontains')
    kota = django_filters.CharFilter(field_name='wadmkk', lookup_expr='icontains')
