from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
import django_filters.rest_framework
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator
from .models import AdministrationRegion
from .serializers.serializers import AdministrationRegionSerializer
from generic_serializers.serializers import ResponseSerializer

class AdministrationRegionViewSet(viewsets.ModelViewSet):
    serializer_class = AdministrationRegionSerializer
    queryset = AdministrationRegion.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['namobj', 'id']
    ordering = ['namobj']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            try:
                region = AdministrationRegion.objects.get(id=request.query_params.get('id'))
                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': 1,
                    'data': AdministrationRegionSerializer(region).data,
                    'error': None,
                })
                return Response(serializer.data)
            except AdministrationRegion.DoesNotExist:
                raise NotFound('Region not found!')

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = AdministrationRegionSerializer(page, many=True)

        return Response(serializer.data)
