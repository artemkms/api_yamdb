from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import signup

router = DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', signup),
]