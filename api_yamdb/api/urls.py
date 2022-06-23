from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import signup, get_token

router = DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]