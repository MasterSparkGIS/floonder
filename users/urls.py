from django.urls import path

from .views import UserViewSet, PublicUserViewSet, CMSRoleViewSet, PublicRoleViewSet, UserProfileViewSet

urlpatterns_cms = [
    path('', UserViewSet.as_view({
        'get': 'list',
        'patch': 'update',
        'delete': 'destroy',
    }), name='cms-users'),
    path('/roles', CMSRoleViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }), name='cms_roles'),
]

urlpatterns_public = [
    path('', PublicUserViewSet.as_view({
        'get': 'list',
    }), name='users'),
    path('/profile', UserProfileViewSet.as_view({
        'get': 'retrieve',
    }), name='profile'),
    path('/roles', PublicRoleViewSet.as_view({
        'get': 'list',
    }), name='roles'),
]
