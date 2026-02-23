from django.shortcuts import render
from rest_framework import generics
from .models import Algorithm
from .serializers import AlgorithmSerializer

class ListAlgorithm(generics.ListAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

class DetailAlgorithm(generics.RetrieveAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

