from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # 1) User anlegen
        user = serializer.save()

        # 2) Token erstellen
        token, _ = Token.objects.get_or_create(user=user)

        # 3) Django-Session Login (setzt Cookie)
        #    so bist du direkt eingeloggt im Browser
        login(request, user)

        # 4) Antwort mit Token + User-Daten
        return Response({
            "token":    token.key,
            "username": user.username,
            "email":    user.email,
            "user_id":  user.id
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    print("REQUEST DATA:", request.data)       
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not serializer.is_valid():
        print("ERRORS:", serializer.errors)    # <— hier ausgeben
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password']
    )
    if not user:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "username": user.username,
        "email": user.email,
        "user_id": user.id
    }, status=status.HTTP_200_OK)
