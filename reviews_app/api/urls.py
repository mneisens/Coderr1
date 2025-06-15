from django.urls import path
from .views import ReviewListCreateAPI, ReviewDetailAPI

urlpatterns = [
    path('reviews/',       ReviewListCreateAPI.as_view(),   name='reviews-list-create'),
    path('reviews/<int:pk>/', ReviewDetailAPI.as_view(),     name='reviews-detail'),
]
