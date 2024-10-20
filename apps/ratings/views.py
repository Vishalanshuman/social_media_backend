from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Rating
from .serializers import RatingSerializer
from apps.common.permissions import IsCustomer
from apps.recipes.models import Recipe
from django.shortcuts import get_object_or_404

class RecipeRatingView(generics.GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomer()]
        return [permissions.AllowAny()]

    def post(self, request, *args, **kwargs):
        try:
            recipe_id = kwargs.get("recipe_id")
            recipe = get_object_or_404(Recipe, id=recipe_id)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(customer=self.request.user, recipe=recipe)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            print(f"Serializer Errors: {serializer.errors}")
            return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response(data={"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    def get(self,request,*args,**kwargs):
            try:
                recipe_id = kwargs.get("recipe_id")
                recipe = get_object_or_404(Recipe, id=recipe_id)
                ratings =  Rating.objects.filter(recipe=recipe)
                serializer = self.serializer_class(ratings,many=True)
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)

