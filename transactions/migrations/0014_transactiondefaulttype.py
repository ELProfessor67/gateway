# Generated by Django 5.0.3 on 2024-03-13 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_transaction_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionDefaultType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('default', models.CharField(max_length=500)),
            ],
        ),
    ]
