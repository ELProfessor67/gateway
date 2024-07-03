from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Questions(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField(default="")
    def __str__(self):
        return self.question
