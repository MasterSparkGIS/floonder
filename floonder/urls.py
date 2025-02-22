
from django.urls import path, include
from auth.urls import urlpatterns as auth_urlpatterns, router as auth_router

from auth.auth import IsSuperUser, IsAdmin
from users.urls import urlpatterns_cms as users_router_cms, urlpatterns_public as users_router_public
urlpatterns = [
    path('api', include([
        path('/auth', include([
            path('', include(auth_urlpatterns)),
            path('/register', include(auth_router.urls)),
        ])),
        path('/cms', include([
            path('/users', include(users_router_cms)),
        ])),
        path('/public', include([
            path('/users', include(users_router_public)),
        ])),
    ])),
]