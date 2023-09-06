# Generated by Django 4.0.6 on 2023-09-05 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_batchs_date_batchs_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shedules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=100)),
                ('first_name', models.CharField(default='', max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=100, verbose_name='Last Name')),
                ('company', models.CharField(default='', max_length=100, verbose_name='Company')),
                ('address', models.CharField(default='', max_length=100, verbose_name='Address')),
                ('city', models.CharField(default='', max_length=100, verbose_name='City')),
                ('state', models.CharField(default='', max_length=100, verbose_name='State')),
                ('zip_code', models.CharField(default='', max_length=10, verbose_name='Zip')),
                ('country', models.CharField(default='', max_length=100, verbose_name='Country')),
                ('phone_number', models.CharField(default='', max_length=20, verbose_name='Phone Number')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('payment_method', models.CharField(default='', max_length=100)),
                ('transaction_type', models.CharField(default='', max_length=100, verbose_name='Transaction Type')),
                ('card_number', models.CharField(default='', max_length=16, verbose_name='Card Number')),
                ('exp_year', models.CharField(default='', max_length=5, verbose_name='Expiration Year')),
                ('exp_month', models.CharField(default='', max_length=5, verbose_name='Expiration Month')),
                ('cvv', models.CharField(default='', max_length=4, verbose_name='CVV')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.TextField(default='')),
                ('amount', models.CharField(default='', max_length=100)),
                ('every', models.IntegerField(default=1)),
                ('gap', models.CharField(max_length=50)),
                ('start', models.DateField(default='')),
                ('end', models.DateField(default='')),
                ('after', models.IntegerField(default=1)),
                ('afterwith', models.IntegerField(default=1)),
            ],
        ),
    ]
