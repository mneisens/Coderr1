from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail  # Annahme: deine OfferDetail kommt aus offers-App

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = fields  # alles read-only, außer beim Erstellen über perform_create

class CreateOrderSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            return OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Angebotsdetail nicht gefunden.")

class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
