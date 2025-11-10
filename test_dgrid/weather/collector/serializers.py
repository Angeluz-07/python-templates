from rest_framework import serializers
from .models import *

class CollectionRequestSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    class Meta:
        model=CollectionRequest
        fields = '__all__'
