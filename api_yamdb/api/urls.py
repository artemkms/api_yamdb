from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from .views import (signup,
                    get_token,
                    UserViewSet,
                    MePage,
                    CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet)
router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/users/me/', MePage.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]



