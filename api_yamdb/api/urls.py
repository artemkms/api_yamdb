from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router_v1 = SimpleRouter()
router_v1.register('v1/categories', CategoryViewSet, basename='categories')
router_v1.register('v1/genres', GenreViewSet, basename='genres')
router_v1.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router_v1.urls))
]

