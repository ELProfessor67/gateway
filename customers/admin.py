from django.contrib import admin

from .models import Customer, AllowField

admin.site.register(Customer)
admin.site.register(AllowField)