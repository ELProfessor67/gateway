# Generated by Django 4.0.6 on 2023-10-31 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_usersbanks'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='by',
            field=models.CharField(default='', max_length=100),
        ),
    ]
