# Generated by Django 5.0.3 on 2024-03-21 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0021_default_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Default_Batch_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('default', models.BooleanField(default=False)),
            ],
        ),
    ]
