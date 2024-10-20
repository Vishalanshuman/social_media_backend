from rest_framework import serializers
from .models import Rating
from apps.users.serializers import GetUserSerializer

class RatingSerializer(serializers.ModelSerializer):
    customer = GetUserSerializer(read_only=True)  # Include customer details

    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'customer', 'rating']
        read_only_fields = ['recipe', 'customer']
