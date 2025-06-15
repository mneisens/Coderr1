# ganz oben
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min
from ..models import Offer, OfferDetail
from .serializers import (
    OfferListSerializer, OfferCreateSerializer, OfferUpdateSerializer,
    OfferDetailSerializer
)
from .permissions import IsBusinessAndOwner

from django.db.models import Min
from rest_framework import generics, filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from ..models import Offer
from .serializers import OfferListSerializer, OfferCreateSerializer
from .filters import OfferFilter

class OfferListAPI(generics.ListCreateAPIView):
    queryset = Offer.objects.all().annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    )
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class    = OfferFilter
    search_fields      = ['title', 'description']
    ordering_fields    = ['updated_at', 'min_price']

    def get_serializer_class(self):
        return OfferCreateSerializer if self.request.method == 'POST' else OfferListSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        # entferne Pagination komplett
        data = self.get_serializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class OfferDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET / PATCH / DELETE eines einzelnen Angebots
    """
    queryset = Offer.objects.all().annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    )
    lookup_field = 'pk'
    permission_classes = [IsBusinessAndOwner]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferListSerializer
        return OfferUpdateSerializer