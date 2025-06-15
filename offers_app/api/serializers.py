from django.db.models import Min
from rest_framework import serializers
from ..models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]
        read_only_fields = ['id']

class OfferListSerializer(serializers.ModelSerializer):
    details            = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='offerdetail-detail',
        lookup_field='pk'
    )
    min_price          = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    min_delivery_time  = serializers.IntegerField(read_only=True)
    user_details       = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user_details(self, obj):
        u = obj.user
        return {
            'first_name': u.first_name or '',
            'last_name':  u.last_name or '',
            'username':   u.username,
        }

class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Ein Angebot muss mindestens 3 Details haben.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(user=self.context['request'].user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

class OfferDetailViewSerializer(OfferListSerializer):
    # baut auf ListSerializer auf, aber zeigt volle URL für details
    pass

class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['title', 'image', 'description']
        extra_kwargs = {'image': {'required': False}}
