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

