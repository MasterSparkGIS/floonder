from django.urls import path

from .views import NewsViewSet, PublishNewsViewSet

urlpatterns = [
    path('', NewsViewSet.as_view({'get': 'list', 'post': 'create'}), name='news-list-create'),
]

urlpatterns_public = [
    path('', PublishNewsViewSet.as_view({'get': 'list'}), name='news-public-list'),
]