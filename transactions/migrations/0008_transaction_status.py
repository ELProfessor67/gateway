# Generated by Django 4.0.6 on 2023-08-27 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(default='Complete', max_length=50),
        ),
    ]
