from rest_framework import serializers
from ..models import Profile

class ProfileDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, default='')
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, default='')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.ChoiceField(
    choices=Profile.TYPE_CHOICES,
    default='customer',
    write_only=True
)


    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at'
        ]

    def update(self, instance, validated_data):
        # update nested user-Felder
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return super().update(instance, validated_data)


class BusinessProfileListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, default='')
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, default='')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type'
        ]


class CustomerProfileListSerializer(serializers.ModelSerializer):
    # extrahiere username und Name aus dem related User
    username    = serializers.CharField(source='user.username')
    first_name  = serializers.CharField(source='user.first_name', default='', allow_blank=True)
    last_name   = serializers.CharField(source='user.last_name',  default='', allow_blank=True)
    # mappe created_at auf uploaded_at im JSON
    uploaded_at = serializers.DateTimeField(source='created_at')
    
    class Meta:
        model  = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'uploaded_at',  
            'type',
        ]