# Generated by Django 5.0.3 on 2024-03-19 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_otp_object_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp_object',
            name='token',
        ),
    ]
