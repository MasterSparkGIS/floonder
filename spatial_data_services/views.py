from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
import django_filters.rest_framework
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator
from .filtersets.adm_filtersets import AdmFilterSet
from .filtersets.rainfall_filtersets import RainfallFilterSet
from .models import AdministrationRegion
from generic_serializers.serializers import ResponseSerializer
from .models_rainfall import Rainfall
from .models_river import River
from .serializers.serializers_adm import AdministrationRegionSerializer
from .serializers.serializers_rainfall import RainfallSerializer
from .serializers.serializers_river import RiverSerializer


class AdministrationRegionViewSet(viewsets.ModelViewSet):
    serializer_class = AdministrationRegionSerializer
    queryset = AdministrationRegion.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = AdmFilterSet
    ordering_fields = ['namobj', 'id']
    ordering = ['namobj']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id') is not None:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(id=request.query_params.get('id'))
            if queryset.count() == 0:
                raise NotFound('Data not found!')
            serializer = self.get_serializer(queryset, many=False)

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': queryset.count(),
                'data': serializer.data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': serializer.data,
            'error': None,
        })

        return Response(serializer.data)

class RainfallViewSet(viewsets.ModelViewSet):
    serializer_class = RainfallSerializer
    queryset = Rainfall.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['fid']
    filterset_class = RainfallFilterSet
    ordering = ['fid']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id') is not None:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(id=request.query_params.get('id'))
            if queryset.count() == 0:
                raise NotFound('Data not found!')
            serializer = self.get_serializer(queryset, many=False)

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': queryset.count(),
                'data': serializer.data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': serializer.data,
            'error': None,
        })

        return Response(serializer.data)

class RiverViewSet(viewsets.ModelViewSet):
    serializer_class = RiverSerializer
    queryset = River.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['id']
    ordering = ['id']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id') is not None:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(id=request.query_params.get('id'))
            if queryset.count() == 0:
                raise NotFound('Data not found!')
            serializer = self.get_serializer(queryset, many=False)

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': queryset.count(),
                'data': serializer.data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': serializer.data,
            'error': None,
        })

        return Response(serializer.data)