# Generated by Django 5.0.3 on 2024-03-19 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_otp_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp_object',
            name='token',
            field=models.CharField(default=None, max_length=200),
        ),
    ]