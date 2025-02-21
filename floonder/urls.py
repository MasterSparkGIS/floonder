
from django.urls import path, include
from auth.urls import urlpatterns as auth_urlpatterns, router as auth_router

from auth.auth import IsSuperUser, IsAdmin
from users.urls import router_cms as users_router_cms, router_public as users_router_public
urlpatterns = [
    path('api/', include([
        path('auth/', include([
            path('', include(auth_urlpatterns)),
            path('register/', include(auth_router.urls)),
        ])),
        path('cms/', include([
            path('users/', include(users_router_cms.urls)),
        ])),
        path('public/', include([
            path('users/', include(users_router_public.urls)),
        ])),
    ])),
]