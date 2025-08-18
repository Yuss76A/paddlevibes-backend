from rest_framework import serializers
from .models import Lake, Photo, Review


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'description', 'lake']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'lake']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("El rating debe ser entre 1 y 5.")
        return value


class LakeSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Lake
        fields = ['id', 'name', 'description', 'latitude', 'longitude',
                  'photos', 'reviews', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
