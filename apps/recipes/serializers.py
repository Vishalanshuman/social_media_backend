from rest_framework import serializers
from .models import Recipe
from apps.users.serializers import GetUserSerializer
from apps.ratings.serializers import RatingSerializer
from apps.ratings.models import Rating
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    # Include seller details using the GetUserSerializer
    seller = GetUserSerializer(read_only=True)
    
    # Include ratings with nested details
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'image', 'seller', 'ratings']
        read_only_fields = ['seller', 'ratings']
