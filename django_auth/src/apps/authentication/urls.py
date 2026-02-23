from django.urls import path
from .views import  UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Endpoint para Login (devuelve Access y Refresh token)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint para renovar el Access Token usando el Refresh Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserDetailView.as_view()),
]