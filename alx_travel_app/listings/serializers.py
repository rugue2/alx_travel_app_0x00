from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'listing', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'location',
            'price_per_night', 'bedrooms', 'bathrooms', 'max_guests',
            'host', 'reviews', 'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return sum(review.rating for review in reviews) / len(reviews)

class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'guest', 'check_in_date', 'check_out_date',
            'number_of_guests', 'total_price', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Check that:
        - check_out_date is after check_in_date
        - number_of_guests does not exceed listing's max_guests
        """
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )

        listing = self.context['listing']
        if data['number_of_guests'] > listing.max_guests:
            raise serializers.ValidationError(
                f"Number of guests cannot exceed listing's maximum capacity of {listing.max_guests}"
            )

        return data