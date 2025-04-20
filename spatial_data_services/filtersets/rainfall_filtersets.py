import django_filters


class RainfallFilterSet(django_filters.FilterSet):
    gridcode = django_filters.NumberFilter(field_name='gridcode', lookup_expr='exact')