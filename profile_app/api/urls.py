from django.urls import path
from .views import profile_view, BusinessProfilesAPI, CustomerProfilesAPI

urlpatterns = [
    path('profile/<pk>/',        profile_view,                 name='profile-detail'),
    path('profiles/business/',   BusinessProfilesAPI.as_view(), name='profiles-business'),
    path('profiles/customer/',   CustomerProfilesAPI.as_view(), name='profiles-customer'),
]