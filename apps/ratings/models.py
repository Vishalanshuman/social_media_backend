from django.db import models
from django.contrib.auth import get_user_model
from apps.recipes.models import Recipe

User = get_user_model()

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('recipe', 'customer') 
        db_table = "comments"

    def __str__(self):
        return self.id
