from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import  UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        # Always returns the user tied to the Token/Session
        return self.request.user