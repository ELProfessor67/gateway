# Generated by Django 5.0.3 on 2024-03-19 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_alter_otp_object_reset_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token_Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('reset_token', models.CharField(default='hhhhhhh', max_length=200)),
            ],
        ),
    ]