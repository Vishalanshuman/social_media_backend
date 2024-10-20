from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,null=False,blank=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Add a unique related_name here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  # Add a unique related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )