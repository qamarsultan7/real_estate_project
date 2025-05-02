

from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # Or list the fields explicitly if you want: ['id', 'giver_id', 'given_id', 'giver_image', 'rating', 'review_text']
