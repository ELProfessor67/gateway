from django.db import models
from transactions.models import Transaction
import datetime
# Create your models here.

class Batchs(models.Model):
    name = models.CharField(max_length=50)
    desciption = models.CharField(max_length=300)
    username = models.CharField(max_length=100)
    transactions = models.CharField(max_length=50000000,default='[]')
    date = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=50,default="Pending")




# shedules 
class Shedules(models.Model):

    # general fields
    custom = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=50,default='')
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
    date = models.DateTimeField(default=datetime.datetime.now)

    # payments fields 
    payment_name = models.CharField(max_length=100,default='')
    # transaction_type = models.CharField(max_length=100, verbose_name='Transaction Type',default='')
    card_number = models.CharField(max_length=16, verbose_name='Card Number' ,default='')
    exp_year = models.CharField(max_length=5, verbose_name='Expiration Year',default='')
    exp_month = models.CharField(max_length=5, verbose_name='Expiration Month',default='')
    cvv = models.CharField(max_length=4, verbose_name='CVV',default='')

    # recustion feilds
    name = models.CharField(max_length=50,default='')
    description = models.TextField(default='')
    amount = models.CharField(max_length=100,default='')
    every = models.IntegerField(default=1)
    gap = models.CharField(max_length=50)
    start = models.DateField(default='')
    end = models.DateField(default='')
    after = models.IntegerField(default=1)
    afterwith = models.IntegerField(default=1)


class OTP_Object(models.Model):
    username = models.CharField(max_length=200)
    otp = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    attempt = models.IntegerField(default=0)
    reset_token = models.CharField(max_length=200,default='hhhhhhh')

class Token_Object(models.Model):
    username = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    reset_token = models.CharField(max_length=200,default='hhhhhhh')
