# from django.urls import path
# from .views import ProfileDetailAPI, BusinessProfilesAPI, CustomerProfilesAPI

# urlpatterns = [
#     path('profile/<int:pk>/', ProfileDetailAPI.as_view(), name='profile-detail'),
#     path('profiles/business/', BusinessProfilesAPI.as_view(), name='profiles-business'),
#     path('profiles/customer/', CustomerProfilesAPI.as_view(), name='profiles-customer'),
# ]

from django.urls import path
from .views import profile_view, BusinessProfilesAPI, CustomerProfilesAPI

urlpatterns = [
    #   path('profile/undefined/', profile_view, name='profile-undefined'),
    path('profile/<int:pk>/',    profile_view,                 name='profile-detail'),
    path('profiles/business/',   BusinessProfilesAPI.as_view(), name='profiles-business'),
    path('profiles/customer/',   CustomerProfilesAPI.as_view(), name='profiles-customer'),
]