# Generated by Django 4.0.6 on 2023-09-09 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_remove_customer_status_customer_cards_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='payment_method',
        ),
    ]
