# Generated by Django 4.0.6 on 2023-09-04 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_remove_customer_bill_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='transaction_type',
        ),
    ]
