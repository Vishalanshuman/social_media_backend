from django.urls import path
from . views import UserRegistrationView,UserLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserRegistrationView.as_view(), name='signup'), 
    path('login/', UserLoginView.as_view(), name='login'), 
]

