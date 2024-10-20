from rest_framework import serializers
from .models import Recipe
from apps.users.serializers import GetUserSerializer
from apps.ratings.serializers import RatingSerializer
from apps.ratings.models import Rating
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'image', 'seller']
        read_only_fields = ['seller']

class GETRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        ratings = serializers.SerializerMethodField()
        seller = serializers.SerializerMethodField()

        model = Recipe
        fields = ['id', 'name', 'description', 'image', 'seller']
        read_only_fields = ['seller']

        def get_ratings(self,obj):
            ratings = Rating.objects.filter(recipe=obj.id)
            return RatingSerializer(ratings,many=True)

        def get_seller(self,obj):
            user = User.objects.get(id=obj.seller)
            return GetUserSerializer(user).data