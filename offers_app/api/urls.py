from django.urls import path
from .views import OfferListAPI, OfferDetailAPI

urlpatterns = [
    path('offers/',         OfferListAPI.as_view(), name='offers-list'),
    path('offerdetails/<int:pk>/', OfferDetailAPI.as_view(), name='offers-detail'),  # passt zu OFFER_DETAIL_URL
]
