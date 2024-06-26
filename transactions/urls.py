from django.urls import path,re_path
from . import views

app_name = 'transactions'

urlpatterns = [
    re_path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('create_ajax/', views.transaction_create_ajax, name='transaction_create_ajax'),

    path('add_api_record/', views.add_api_record, name='add_api_record'),
    path('<int:pk>/update/', views.transaction_update, name='transaction_update'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('shuffing_merchant_key/', views.limiter, name='shuffling keys'),
    path('add_bank_account/', views.add_bank_account, name='add_bank_account'),
    path('my-team/', views.my_team, name='my team'),
    path('add-member/', views.add_member, name='my team'),
    path('show_bank/', views.show_bank, name='show_bank'),
    path('edit-bank-verify/', views.edit_bank_verify, name='edit_bank_verify'),
    path('default_transaction_type/', views.default_transaction_type, name='default_transaction_type'),
    path('verify-user/', views.verify_user, name='verify-user'),
    path('general/', views.general, name='verify-user'),
    path('batch-setting/', views.batchsetting, name='verify-user'),
    path('team-activity/', views.activity, name='activity'),
]