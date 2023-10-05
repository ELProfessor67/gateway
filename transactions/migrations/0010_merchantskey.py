# Generated by Django 4.0.6 on 2023-10-05 02:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_approvemails'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantsKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=uuid.uuid4, max_length=50)),
                ('username', models.CharField(max_length=200)),
            ],
        ),
    ]
