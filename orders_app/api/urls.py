from django.urls import path
from .views import (
    OrderListCreateAPI, OrderDetailAPI,
    OrderCountAPI, CompletedOrderCountAPI
)

urlpatterns = [
    path('orders/',               OrderListCreateAPI.as_view(),       name='orders-list-create'),
    path('orders/<int:pk>/',      OrderDetailAPI.as_view(),           name='orders-detail'),
    path('order-count/<int:business_user_id>/',
                                  OrderCountAPI.as_view(),            name='orders-in-progress-count'),
    path('completed-order-count/<int:business_user_id>/',
                                  CompletedOrderCountAPI.as_view(),   name='orders-completed-count'),
]
