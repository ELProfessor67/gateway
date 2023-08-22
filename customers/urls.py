from django.urls import path,re_path
from . import views

app_name = 'customers'

urlpatterns = [
    re_path('customers_list/', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('add_api_record/', views.customer_detail, name='add_api_record'),
    path('<int:pk>/update/', views.customer_update, name='customer_update'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
]