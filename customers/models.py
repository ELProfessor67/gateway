from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=20)
    bill_company = models.CharField(max_length=100)
    bill_first_name = models.CharField(max_length=50)
    bill_last_name = models.CharField(max_length=50)
    recurring_schedule = models.CharField(max_length=50)
    bill_phone_number = models.CharField(max_length=20)
    email = models.EmailField()
