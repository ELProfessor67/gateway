from django.db import models
import datetime
import re
from uuid import uuid4
import random

class Transaction(models.Model):
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
    amount = models.CharField(max_length=100,default='')
    payment_method = models.CharField(max_length=100,default='')
    transaction_type = models.CharField(max_length=100, verbose_name='Transaction Type',default='')
    card_number = models.CharField(max_length=16, verbose_name='Card Number' ,default='')
    exp_year = models.CharField(max_length=5, verbose_name='Expiration Year',default='')
    exp_month = models.CharField(max_length=5, verbose_name='Expiration Month',default='')
    cvv = models.CharField(max_length=4, verbose_name='CVV',default='')
    email = models.EmailField(max_length=100, verbose_name='Email',default='')
    transaction_id = models.CharField(max_length=150, verbose_name='Transaction_id',default='')
    date = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(default='Complete',max_length=50)
    by = models.CharField(max_length=100,default='')

    def get_card_company(self):
        card_number = self.card_number
        # Define regular expressions for different card companies
        patterns = {
            'Visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
            'Mastercard': r'^5[1-5][0-9]{14}$',
            "Amex": r'^3[47][0-9]{13}$',
            "Discover": r'^6(?:011|5[0-9]{2})[0-9]{12}$',
            "JCB": r'^(?:2131|1800|35[0-9]{3})[0-9]{11}$'
            # Add more patterns for other card companies here
        }

        for company, pattern in patterns.items():
            if re.match(pattern, card_number):
                return company
        # If no company is detected, return 'unknown'
        return 'Amex'
    

def isunique(card_number,username):
        all_transaction = Transaction.objects.all().exclude(username=username)

        unique = True

        for i in all_transaction:
            # print(i.card_number,card_number)
            if i.card_number == card_number:
                unique = False
        
        return unique


class ApproveMails(models.Model):
    email = models.CharField(max_length=300)
    status = models.CharField(choices=(('approve','Approve'),('disapprove','Disapprove')),default='1',max_length=200)
    

class MerchantsKey(models.Model):
     key = models.CharField(max_length=50,default=uuid4)
     username = models.CharField(max_length=200)

     def shuffling_key(self):
          parts = self.key.split('-')
          shuffled_parts = random.sample(parts[:-1],len(parts)-1)
          
          return '-'.join(shuffled_parts)+'-'+parts[-1]

class UserBanks(models.Model):
     username = models.CharField(max_length=200)
     bank_name = models.CharField(max_length=500)
     account_id = models.CharField(max_length=500)
     account_holder_name = models.CharField(max_length=200)
     IFSC = models.CharField(max_length=100)

class UsersBanks(models.Model):
     username = models.CharField(max_length=200)
     bank_name = models.CharField(max_length=500)
     bank_address = models.CharField(max_length=500)
     account_number = models.CharField(max_length=500,default='09865645')
     account_holder_name = models.CharField(max_length=200)
     account_holder_address = models.CharField(max_length=500)
     routing_number = models.CharField(max_length=100)
     bic_code = models.CharField(max_length=100,default='3454')