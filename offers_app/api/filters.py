# offers_app/api/filters.py
import django_filters
from ..models import Offer

class OfferFilter(django_filters.FilterSet):
    creator_id         = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    min_price          = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte')
    max_price          = django_filters.NumberFilter(field_name='details__price', lookup_expr='lte')
    max_delivery_time  = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model  = Offer
        fields = ['creator_id', 'min_price', 'max_price', 'max_delivery_time']
