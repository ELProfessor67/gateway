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
]