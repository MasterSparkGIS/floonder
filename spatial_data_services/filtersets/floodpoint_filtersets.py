import django_filters

from spatial_data_services.utils import month_dict


class FloodPointFilterset(django_filters.FilterSet):
    kelurahan = django_filters.CharFilter(field_name='namobj', lookup_expr='iexact')
    kecamatan = django_filters.CharFilter(field_name='wadmkc', lookup_expr='iexact')
    kota = django_filters.CharFilter(field_name='wadmkk', lookup_expr='iexact')
    provinsi = django_filters.CharFilter(field_name='wadmpr', lookup_expr='icontains')
    month = django_filters.NumberFilter(method='filter_by_month')
    year = django_filters.NumberFilter(field_name='year', lookup_expr='iexact')

    def filter_by_month(self, queryset, name, value):
        try:
            month_name = month_dict[value]
            return queryset.filter(month__iexact=month_name)
        except (ValueError, IndexError):
            return queryset.none()
