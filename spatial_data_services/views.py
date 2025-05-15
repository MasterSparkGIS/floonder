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
from .filtersets.floodpoint_filtersets import FloodPointFilterset
from .filtersets.rainfall_filtersets import RainfallFilterSet
from .filtersets.river_filtersets import RiverFilterset
from .models import AdministrationRegion
from generic_serializers.serializers import ResponseSerializer
from .models_dem import DigitalElevationModel
from .models_floodpoint import FloodPoint
from .models_kosan import Kosan
from .models_lake import Lake
from .models_property import Property
from .models_rainfall import Rainfall
from .models_river import River
from .models_slope import Slope
from .serializers.serializers_adm import AdministrationRegionSerializer
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

class FloodPointViewSet2(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint returning flood-risk points for a given month.
    Uses lazy QuerySets and Q() filters to defer evaluation until iteration.
    """
    serializer_class = FloodPointSerializer
    lookup_field = 'month'

    def get_queryset(self):
        month = self.kwargs['month']

        # Base lazy querysets
        rain_qs = Rainfall.objects.filter(month=month)
        admins = AdministrationRegion.objects.filter(
            Q(geom__intersects=rain_qs.values('geom'))
        )

        # Grab one instance of each raster (defer loading the blob until needed)
        dem = DigitalElevationModel.objects.defer('raster').first()
        slope = Slope.objects.defer('raster').first()

        rivers = River.objects.all()
        lakes = Lake.objects.all()

        # Build in-memory list of FloodPoint objects (unsaved)
        points = []
        # Precompute threshold_dict per admin
        threshold_dict = {}
        for admin in admins:
            # Compute DEM stats per admin polygon
            stats = zonal_stats(
                [admin.geom.geojson],
                dem.raster.path,
                stats=["min", "max", "mean", "std"],
                geojson_out=False
            )[0]
            threshold_dict[admin.wadmkk] = stats["mean"] - 0.5 * stats["std"]

        for admin in admins.iterator():
            # get all rain‐grid polys intersecting this admin
            for grid in rain_qs.filter(geom__intersects=admin.geom):
                # fetch zonal DEM stats for each intersected piece
                stats = zonal_stats(
                    [mapping(admin.geom)],
                    dem.raster.path,
                    stats=["min", "max", "mean", "std"],
                    geojson_out=True
                )
                for feat in stats:
                    props = feat['properties']
                    dem_min = props['min']
                    dem_max = props['max']
                    dem_mean = props['mean']
                    dem_std = props['std']

                    # simple flood‐potential check
                    if grid.gridcode < 2:
                        continue

                    # compute centroid point for distance calc
                    pt = GEOSGeometry(feat['geometry']).centroid

                    # mask out the DEM and slope around the polygon to find lowest spot
                    with rasterio.open(dem.raster.path) as src_dem, \
                         rasterio.open(slope.raster.path) as src_slope:

                        try:
                            out_dem, t_dem = mask(src_dem, [mapping(admin.geom)], crop=True)
                            out_slope, t_sl = mask(src_slope, [mapping(admin.geom)], crop=True)
                        except Exception:
                            continue

                    data_dem = out_dem[0].astype(float)
                    data_slope = out_slope[0].astype(float)
                    nod = src_dem.nodata
                    if nod is not None:
                        data_dem[data_dem == nod] = np.nan
                    nod_s = src_slope.nodata
                    if nod_s is not None:
                        data_slope[data_slope == nod_s] = np.nan

                    if np.all(np.isnan(data_dem)):
                        continue

                    # find flood‐elevation and its coords
                    idx_min = np.unravel_index(np.nanargmin(data_dem), data_dem.shape)
                    flood_elev = float(np.nanmin(data_dem))
                    x, y = rasterio.transform.xy(t_dem, *idx_min)
                    flood_pt = Point(x, y)

                    avg_slope = float(np.nanmean(data_slope))

                    # distance to nearest river
                    dist_r = min(r.geom.distance(flood_pt) for f in rivers)
                    if dist_r <= 20:
                        continue

                    # skip near lakes
                    if any(l.geom.buffer(30).contains(flood_pt) for l in lakes):
                        continue

                    # river‐side elevation
                    # pick nearest river segment, buffer, stat
                    nearest = min(rivers, key=lambda r: r.geom.distance(flood_pt))
                    buff = nearest.geom.buffer(10)
                    river_stats = zonal_stats([mapping(buff)], dem.raster.path, stats=["mean"])[0]
                    river_elev = river_stats.get("mean", np.nan)
                    if np.isnan(river_elev):
                        continue

                    # risk scoring
                    # (use your calculate_risk_score & classify_risk_from_score logic here)
                    # ... for brevity, we’ll call helper functions you define elsewhere ...

                    # assemble the FloodPoint instance
                    fp = FloodPoint(
                        admin=admin,
                        geom=flood_pt,
                        month=month,
                        dem_min=dem_min,
                        dem_max=dem_max,
                        dem_mean=dem_mean,
                        dem_std=dem_std,
                        avg_slope=avg_slope,
                        dist_to_river=dist_r,
                        flood_elev=flood_elev,
                        river_elev=river_elev,
                        risk_score=0,    # replace with real score
                        risk_level='',   # replace with real classification
                        year=2025
                    )
                    points.append(fp)

        return points

    def list(self, request, *args, **kwargs):
        pts = self.get_queryset()
        serializer = self.get_serializer(pts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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