from django.db import models
from apps.common.tasks import resize_recipe_image
from django.contrib.auth import get_user_model
from apps.users.serializers import UserRegistrationSerializer

User = get_user_model()

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    class Meta:
        db_table = "recipes"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_recipe_image.delay(self.image.name)
