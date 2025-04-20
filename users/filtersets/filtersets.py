from datetime import datetime

import django_filters
from django.db.models import Q
from rest_framework import filters


class UserSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        if search_param:
            queryset = queryset.filter(Q(name__icontains=search_param) | Q(nim__icontains=search_param))
        return queryset


class UserFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='active')
    role = django_filters.CharFilter(field_name='role_id', lookup_expr='exact')
    role_name = django_filters.CharFilter(field_name='role_id__name', lookup_expr='icontains')
    role_name_exact = django_filters.CharFilter(field_name='role_id__name', lookup_expr='exact')


class RoleFilterSet(django_filters.FilterSet):
    date_field = django_filters.CharFilter(method='filter_date_field')
    start_date = django_filters.CharFilter(method='filter_start_date')
    end_date = django_filters.CharFilter(method='filter_endDate')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    date_field_value = "created_at"

    def filter_date_field(self, queryset, name, value):
        self.date_field_value = "created_at"

        return queryset

    def filter_start_date(self, queryset, name, value):
        try:
            start_date = datetime.strptime(value, "%d-%m-%Y %H:%M")
            return queryset.filter(**{f"{self.date_field_value}__gte": start_date.strftime('%Y-%m-%d %H:%M')})
        except ValueError:
            return queryset.none()

    def filter_end_date(self, queryset, name, value):
        try:
            end_date = datetime.strptime(value, "%d-%m-%Y %H:%M")
            return queryset.filter(**{f"{self.date_field_value}__lte": end_date.strftime('%Y-%m-%d %H:%M')})
        except ValueError:
            return queryset.none()
