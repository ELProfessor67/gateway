# Generated by Django 4.0.6 on 2023-10-04 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_transaction_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApproveMails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('approve', 'Approve'), ('disapprove', 'Disapprove')], default='1', max_length=200)),
            ],
        ),
    ]
