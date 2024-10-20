from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer
from apps.common.permissions import IsSeller
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()

class RecipeListView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsSeller()]
        return [permissions.AllowAny()]

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user)  

    def perform_destroy(self, instance):
        if instance.seller != self.request.user:
            return Response(data={"message":"You do not have permission to delete this recipe."},status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
