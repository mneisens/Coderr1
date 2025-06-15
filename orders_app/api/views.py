from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from auth_app import models
from ..models import Order
from .serializers import (
    OrderSerializer, CreateOrderSerializer, StatusUpdateSerializer
)
from .permissions import IsCustomer, IsBusinessAndOwner
from django.db.models import Q

class OrderListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        offer_detail = serializer.validated_data['offer_detail_id']
        # nur Kunde darf hierher (Absicherung durch IsCustomer)
        order = Order.objects.create(
            customer_user=self.request.user,
            business_user=offer_detail.offer.business_user,
            title=offer_detail.offer.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer.offer_type,
            status='in_progress'
        )
        self._created_order = order

    def create(self, request, *args, **kwargs):
        # prüfe Permission vor perform_create
        if request.method == 'POST':
            self.check_permissions(request)
            if not IsCustomer().has_permission(request, self):
                return Response({'detail': 'Nur Kunden dürfen bestellen.'},
                                status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        # nach erfolgreichem POST das komplette Order-Objekt serialisieren
        if request.method == 'POST' and response.status_code == status.HTTP_201_CREATED:
            data = OrderSerializer(self._created_order).data
            response.data = data
        return super().finalize_response(request, response, *args, **kwargs)


class OrderDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    lookup_field = 'pk'
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsBusinessAndOwner()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return StatusUpdateSerializer
        return OrderSerializer


class OrderCountAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, business_user_id):
        count = Order.objects.filter(
            business_user__id=business_user_id,
            status='in_progress'
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, business_user_id):
        count = Order.objects.filter(
            business_user__id=business_user_id,
            status='completed'
        ).count()
        return Response({'completed_order_count': count})

# orders_app/api/views.py

from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Order
from .serializers import OrderSerializer, CreateOrderSerializer

class OrderListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by('-created_at')

    def get_serializer_class(self):
        return CreateOrderSerializer if self.request.method == 'POST' else OrderSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = self.get_serializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)
