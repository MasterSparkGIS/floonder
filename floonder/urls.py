from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from auth.urls import urlpatterns as auth_urlpatterns, router as auth_router
from users.urls import urlpatterns_cms as users_router_cms, urlpatterns_public as users_router_public
from spatial_data_services.urls import urlpatterns as gis_urlpatterns

urlpatterns = [
    path('api', include([
        path('/auth', include([
            path('/', include(auth_urlpatterns)),
            path('/register', include(auth_router.urls)),
        ])),
        path('/cms', include([
            path('/users', include(users_router_cms)),
        ])),
        path('/public', include([
            path('/users', include(users_router_public)),
            path('/gis', include(gis_urlpatterns)),
        ])),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)