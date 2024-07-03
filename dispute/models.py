from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Dispute(models.Model):
    DISPUTE_TYPE_CHOICES = [
        ('Transaction', 'Transaction'),
        ('Service', 'Service'),
        ('Other', 'Other'),
    ]
    
    type = models.CharField(max_length=50, choices=DISPUTE_TYPE_CHOICES)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.description[:50]}"

