from django.db import models

# Create your models here.
class CollectionRequest(models.Model):    
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    city_weather_info = models.JSONField(default=dict)
