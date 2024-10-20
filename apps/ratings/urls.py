from django.urls import path
from .views import RecipeRatingView

urlpatterns = [
    path('<int:recipe_id>/rate/', RecipeRatingView.as_view(), name='recipe-rate'),  # POST /recipes/{id}/rate/
    path('<int:recipe_id>/ratings/', RecipeRatingView.as_view(), name='recipe-ratings'),  # GET /recipes/{id}/ratings/
]
