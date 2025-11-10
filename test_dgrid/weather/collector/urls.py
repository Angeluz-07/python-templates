from django.urls import include, path
from rest_framework import routers
from .views import *

urlpatterns = [    
	path('',collection_request), 
	path('collection-request/',collection_request),    	
	path('collection-request/<int:pk>',get_collection_request), 
	path('collection-request/<int:pk>/progress',collection_request_creation_progress),
]