from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Profile
from .serializers import (
    ProfileDetailSerializer,
    BusinessProfileListSerializer,
    CustomerProfileListSerializer
)
from .permissions import IsOwnerOrReadOnly
from rest_framework import status, generics, mixins

# User = get_user_model()

# class ProfileDetailAPI(generics.RetrieveUpdateAPIView):
#     """
#     GET /api/profile/<any>/  liefert immer ein Array mit genau einem Profil-Dict.
#     PATCH /api/profile/<any>/ updated und liefert auch ein Array.
#     """
#     serializer_class   = ProfileDetailSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#     lookup_field       = 'user'         # wenn du per user__pk suchst
#     lookup_url_kwarg   = 'pk'

#     def get_object(self):
#         # Immer das Profil des eingeloggten Users, neu angelegt falls nötig
#         profile, _ = Profile.objects.get_or_create(
#             user=self.request.user,
#             defaults={
#                 'type': 'customer',
#                 'file': None,
#                 'location': '',
#                 'tel': '',
#                 'description': '',
#                 'working_hours': '',
#             }
#         )
#         return profile

#     def get(self, request, *args, **kwargs):
#         # Hol das Profil, serialisiere es und gib es als 1-Element-Array zurück
#         inst = self.get_object()
#         data = self.get_serializer(inst).data
#         return Response([data], status=status.HTTP_200_OK)

#     def patch(self, request, *args, **kwargs):
#         inst = self.get_object()
#         serializer = self.get_serializer(inst, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response([serializer.data], status=status.HTTP_200_OK)


from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from ..models import Profile
from .serializers import ProfileDetailSerializer

@api_view(['GET', 'PATCH'])
# @authentication_classes([BaseAuthentication])    # keine DRF-Auth, wir parsen manuell
@authentication_classes([]) 
@permission_classes([AllowAny])                  # jede Anfrage darf rein
def profile_view(request, pk=None):
    """
    Liefert IMMER ein JSON-Array zurück:
    - GET → [] oder [ {...Profil...} ] (nie 401/404/500)
    - PATCH → 401 ohne gültigen Token, ansonsten [ {...aktualisiertes Profil...} ]
    """
    # 1) Manuelles Token-Parsing
    auth = request.META.get('HTTP_AUTHORIZATION', '')
    user = None
    if auth.startswith('Token '):
        token_key = auth.split(' ', 1)[1]
        try:
            user = Token.objects.get(key=token_key).user
        except Token.DoesNotExist:
            user = None

    # 2) Wenn GET und kein gültiger User → leeres Array
    if request.method == 'GET' and user is None:
        return Response([], status=status.HTTP_200_OK)

    # 3) Wenn PATCH und kein gültiger User → 401
    if request.method == 'PATCH' and user is None:
        return Response({'detail': 'Authentication required.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    # Ab hier: entweder PATCH mit User oder GET mit gültigem User
    request.user = user  # setzt user für das ORM

    # Wrappe alles in try/except, damit selbst bei 500-Fehlern GET → []
    try:
        # Profil holen oder neu anlegen
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                'type': 'customer',
                'file': None,
                'location': '',
                'tel': '',
                'description': '',
                'working_hours': '',
            }
        )
        # PATCH: Aktualisierung
        if request.method == 'PATCH':
            serializer = ProfileDetailSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = ProfileDetailSerializer(profile)

        data = [serializer.data]

        return Response(data, status=status.HTTP_200_OK)

    except Exception:
        # Fängt alle unerwarteten Fehler ab und gibt für GET ein leeres Array zurück
        if request.method == 'GET':
            return Response([], status=status.HTTP_200_OK)
        # Für PATCH weiterwerfen oder als 500 melden
        return Response({'detail': 'Internal error.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessProfilesAPI(ListAPIView):
    queryset = Profile.objects.filter(type='business').select_related('user')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        qs   = self.get_queryset()
        data = self.get_serializer(qs, many=True).data
        return Response(data, status=200)


class CustomerProfilesAPI(ListAPIView):
    queryset = Profile.objects.filter(type='customer').select_related('user')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None      # ganz ausschalten

    def list(self, request, *args, **kwargs):
        qs   = self.get_queryset()
        data = self.get_serializer(qs, many=True).data
        return Response(data, status=200)