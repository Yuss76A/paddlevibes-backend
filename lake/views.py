from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lake, Photo, Review
from .serializers import PhotoSerializer, LakeSerializer, ReviewSerializer
from django.db.models import Avg
from rest_framework.decorators import action

class LakeViewSet(viewsets.ModelViewSet):
    queryset = Lake.objects.prefetch_related('photos', 'reviews').all()
    serializer_class = LakeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        lake = self.get_object()
        return Response({
            'photos_count': lake.photos.count(),
            'average_rating': lake.reviews.aggregate(Avg('rating'))['rating__avg']
        })

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.select_related('lake').all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('lake', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
