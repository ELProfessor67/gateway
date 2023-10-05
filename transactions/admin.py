from django.contrib import admin
from .models import Transaction, ApproveMails,MerchantsKey
# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    # list_display=('trasnsaction_id','description','timestamp','currency','payment_method','status','amount')
    list_display=('first_name','last_name','company','address','city','state','zip_code','country','phone_number','amount','payment_method','transaction_type','card_number','exp_year','exp_month','cvv','email','transaction_id','username','date')
    search_fields = ('username','first_name','last_name','company','address','city','state','zip_code','country','phone_number','amount','payment_method','transaction_type','card_number','exp_year','exp_month','cvv','email','transaction_id','date')
    list_filter = ['date']

class ApproveMailsAdmin(admin.ModelAdmin):
    # list_display=('trasnsaction_id','description','timestamp','currency','payment_method','status','amount')
    list_display=('email','status')
    # search_fields = ('email')
    list_filter = ['status']

admin.site.register(Transaction,TransactionsAdmin)
admin.site.register(ApproveMails,ApproveMailsAdmin)
admin.site.register(MerchantsKey)