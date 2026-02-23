from django.urls import path
from .views import ListAlgorithm, DetailAlgorithm

urlpatterns = [
    path('algorithms/<int:pk>/', DetailAlgorithm.as_view()),
    path('algorithms/', ListAlgorithm.as_view()),
]
