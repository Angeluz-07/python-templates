from django.db import models
import uuid

    
class Algorithm(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self): 
        return self.name
