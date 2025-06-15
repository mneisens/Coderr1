from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewerOrReadOnly

class ReviewListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # … filter_backends, etc. …

    def list(self, request, *args, **kwargs):
        qs   = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class ReviewDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('business_user','reviewer').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewerOrReadOnly]
    lookup_field = 'pk'
