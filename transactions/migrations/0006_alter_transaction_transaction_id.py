# Generated by Django 4.0.6 on 2023-08-24 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transaction_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default='', max_length=150, verbose_name='Transaction_id'),
        ),
    ]
