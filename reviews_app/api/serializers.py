from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating muss zwischen 1 und 5 liegen.")
        return value

    def validate(self, data):
        request = self.context['request']
        business_user = data.get('business_user')
        reviewer = request.user

        # Nur Kunden dürfen bewerten
        if reviewer.profile.type != 'customer':
            raise serializers.ValidationError("Nur Kunden dürfen Bewertungen erstellen.")

        # Einmal-Pro-User-Regel
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("Du hast bereits eine Bewertung für diesen Nutzer abgegeben.")

        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
