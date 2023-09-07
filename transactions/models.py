from django.db import models
import datetime
import re

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
        return 'Visa'
    