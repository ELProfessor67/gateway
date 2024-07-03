from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Invoices(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    amount = models.IntegerField(default=0)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.name
