from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from auth.auth import IsAdmin, IsSuperUser
from news.models import News
from news.serializers.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            news_id = request.query_params.get('id')
            try:
                news_item = News.objects.get(id=news_id)
            except News.DoesNotExist:
                return Response({'error': 'News item not found'}, status=404)

            serializer = self.get_serializer(news_item)
            return Response(serializer.data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

class PublishNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            news_id = request.query_params.get('id')
            try:
                news_item = News.objects.get(id=news_id, published=True)
            except News.DoesNotExist:
                return Response({'error': 'News item not found'}, status=404)

            serializer = self.get_serializer(news_item)
            return Response(serializer.data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)