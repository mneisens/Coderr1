from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from reviews_app.models import Review
from profile_app.models import Profile
from offers_app.models import Offer

class BaseInfoAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Anzahl aller Reviews
        review_count = Review.objects.count()

        # Durchschnittliche Bewertung (auf eine Nachkommastelle gerundet)
        avg = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        average_rating = round(avg, 1)

        # Anzahl aller Business-Profile
        business_profile_count = Profile.objects.filter(type='business').count()

        # Anzahl aller Offers
        offer_count = Offer.objects.count()

        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)
