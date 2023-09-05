from django.contrib import admin
from .models import Batchs
# Register your models here.

class BatchsAdmin(admin.ModelAdmin):
    # list_display=('trasnsaction_id','description','timestamp','currency','payment_method','status','amount')
    list_display=('name','desciption','username','date','status')
    search_fields = ('name','description','username')

admin.site.register(Batchs,BatchsAdmin)