from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=Profile.TYPE_CHOICES,
        default='customer',
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.pop('type')
        user = User.objects.create_user(**validated_data)
        # Profil hier direkt anlegen
        Profile.objects.create(
            user=user,
            type=user_type,
            file=None,
            location='',
            tel='',
            description='',
            working_hours=''
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
