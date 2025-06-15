# stats_app/urls.py
from django.urls import path
from .views import BaseInfoAPI

urlpatterns = [
    path('base-info/', BaseInfoAPI.as_view(), name='base-info'),
]
