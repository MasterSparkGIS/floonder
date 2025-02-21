from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PublicUserViewSet, CMSRoleViewSet, PublicRoleViewSet, UserProfileViewSet

router_cms = DefaultRouter()
router_cms.register(r'', UserViewSet, basename='cms-users')
router_cms.register(r'roles', CMSRoleViewSet, basename='cms-roles')

router_public = DefaultRouter()
router_public.register(r'', PublicUserViewSet, basename='public-users')
router_public.register(r'roles', PublicRoleViewSet, basename='public-roles')
router_public.register(r'profile', UserProfileViewSet, basename='public-profile')