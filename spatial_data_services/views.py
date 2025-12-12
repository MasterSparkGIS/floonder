import pandas as pd
import rasterio
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q
from rasterio.mask import mask
from rasterstats import zonal_stats
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
import django_filters.rest_framework
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from shapely.geometry.geo import mapping
from shapely.geometry.point import Point

from auth.auth import IsSuperUser
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator
from .filtersets.adm_filtersets import AdmFilterSet
from .filtersets.area_filtersets import FloodAreaFilterSet
from .filtersets.floodpoint_filtersets import FloodPointFilterset
from .filtersets.rainfall_filtersets import RainfallFilterSet
from .filtersets.river_filtersets import RiverFilterset
from .models import AdministrationRegion
from generic_serializers.serializers import ResponseSerializer
from .models_dem import DigitalElevationModel
from .models_floodarea import FloodArea
from .models_floodpoint import FloodPoint
from .models_kosan import Kosan
from .models_lake import Lake
from .models_property import Property
from .models_rainfall import Rainfall
from .models_river import River
from .models_slope import Slope
from .serializers.serializers_adm import AdministrationRegionSerializer
from .serializers.serializers_area import FloodAreaSerializer
from .serializers.serializers_dem import DigitalElevationModelSerializer
from .serializers.serializers_flood_point import FloodPointSerializer
from .serializers.serializers_kosan import KosanSerializer
from .serializers.serializers_lake import LakeSerializer
from .serializers.serializers_property import PropertySerializer
from .serializers.serializers_rainfall import RainfallSerializer
from .serializers.serializers_river import RiverSerializer
from .serializers.serializers_slope import SlopeSerializer

import numpy as np

from .utils import month_dict


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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.query_params.get('month'):
            context['month'] = self.request.query_params.get('month')
        else:
            context['month'] = pd.to_datetime('now').month

        return context

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
        if request.query_params.get('month') is not None:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(id=request.query_params.get('month'))
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

        get_current_month = pd.to_datetime('now').month

        month = month_dict.get(get_current_month)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(month=month)
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
    filterset_class = RiverFilterset
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

class LakeViewSet(viewsets.ModelViewSet):
    serializer_class = LakeSerializer
    queryset = Lake.objects.all()
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

class DEMViewSet(viewsets.ModelViewSet):
    serializer_class = DigitalElevationModelSerializer
    queryset = DigitalElevationModel.objects.all()
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

class SlopeViewSet(viewsets.ModelViewSet):
    serializer_class = SlopeSerializer
    queryset = Slope.objects.all()
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

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
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

class FloodPointViewSet(viewsets.ModelViewSet):
    serializer_class = FloodPointSerializer
    queryset = FloodPoint.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = FloodPointFilterset
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if self.request.query_params.get('month') is None:
            get_current_month = pd.to_datetime('now').month
            month = month_dict.get(get_current_month)
            queryset = queryset.filter(month=month)

        if self.request.query_params.get('year') is None:
            get_current_year = pd.to_datetime('now').year
            queryset = queryset.filter(year=get_current_year)

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

class KosanViewSet(viewsets.ModelViewSet):
    serializer_class = KosanSerializer
    queryset = Kosan.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    pagination_class = GenericPaginator
    authentication_classes = [
        JWTAuthentication
    ]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsSuperUser()]
        return [AllowAny()]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FloodAreaViewSet(viewsets.ModelViewSet):
    serializer_class = FloodAreaSerializer
    queryset = FloodArea.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = FloodAreaFilterSet
    ordering_fields = ['id', 'risk_score', 'desa']
    ordering = ['id']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('bulan') is None:
            get_current_month = pd.to_datetime('now').month
            month_name = month_dict.get(get_current_month)
            queryset = queryset.filter(bulan__icontains=month_name)

        if request.query_params.get('tahun') is None:
            get_current_year = pd.to_datetime('now').year
            queryset = queryset.filter(tahun=get_current_year)

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