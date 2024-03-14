from django.db import models
import datetime
from uuid import uuid1

class Customer(models.Model):
    username = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, verbose_name='First Name',default='')
    last_name = models.CharField(max_length=100, verbose_name='Last Name',default='')
    company = models.CharField(max_length=100, verbose_name='Company',default='')
    address = models.CharField(max_length=100, verbose_name='Address',default='')
    city = models.CharField(max_length=100, verbose_name='City',default='')
    state = models.CharField(max_length=100, verbose_name='State',default='')
    zip_code = models.CharField(max_length=10, verbose_name='Zip',default='')
    country = models.CharField(max_length=100, verbose_name='Country',default='')
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number',default='')
    # amount = models.CharField(max_length=100,default='')
    # payment_method = models.CharField(max_length=100,default='')
    card_number = models.CharField(max_length=16, verbose_name='Card Number' ,default='')
    exp_year = models.CharField(max_length=5, verbose_name='Expiration Year',default='')
    exp_month = models.CharField(max_length=5, verbose_name='Expiration Month',default='')
    cvv = models.CharField(max_length=4, verbose_name='CVV',default='')
    email = models.EmailField(max_length=100, verbose_name='Email',default='')
    # transaction_type = models.CharField(max_length=100, verbose_name='Transaction Type',default='')
    date = models.DateTimeField(default=datetime.datetime.now)
    # status = models.CharField(default='Complete',max_length=50)
    customer_id = models.CharField(max_length=150, verbose_name='Transaction_id',default=uuid1)

    cards = models.TextField(default='[]')



class AllowField(models.Model):
    username = models.CharField(max_length=100, default='')
    first_name = models.BooleanField(default=True)
    last_name = models.BooleanField(default= True)
    company = models.BooleanField(default= True)
    address = models.BooleanField(default= True)
    city = models.BooleanField(default= True)
    state = models.BooleanField(default= True)
    zip_code = models.BooleanField(default= True)
    country = models.BooleanField(default= True)
    phone_number = models.BooleanField(default= True)
    card_number = models.BooleanField(default= True)
    exp_year = models.BooleanField(default= True)
    exp_month = models.BooleanField(default= True)
    cvv = models.BooleanField(default= True)
    email = models.BooleanField(default= True)


# first_name = models.BooleanField(default= True)
#     last_name = 
#     company = 
#     address = 
#     city = 
#     state = 
#     zip_code = 
#     country = 
#     phone_number = 
#     card_number = 
#     exp_year = 
#     exp_month = 
#     cvv = 
#     email = 