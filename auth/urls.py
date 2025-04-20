from django.urls import path
from rest_framework.routers import DefaultRouter

from auth.views import JwtObtain, RefreshToken, RegisterViewSet

router = DefaultRouter()
router.register(r'', RegisterViewSet, basename='register')

urlpatterns = [
    path('login', JwtObtain.as_view(), name='token_obtain'),
    path('refresh', RefreshToken.as_view(), name='token_refresh'),
]
