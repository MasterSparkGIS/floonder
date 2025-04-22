import django_filters
from coreschema import Union
from django.db.models import Q

from spatial_data_services.models_administration_region import AdministrationRegion
from spatial_data_services.models_river import River


class RiverFilterset(django_filters.FilterSet):
    kota = django_filters.CharFilter(method='filter_by_kota')

    class Meta:
        model = River
        fields = ['kota']

    def filter_by_kota(self, queryset, name, value):
        regions = AdministrationRegion.objects.filter(wadmkk__iexact=value)
        if not regions.exists():
            return queryset.none()

        q = Q()
        for region in regions:
            q |= Q(geom__intersects=region.geom)
        return queryset.filter(q)