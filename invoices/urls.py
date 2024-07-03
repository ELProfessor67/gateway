from django.urls import path
from .views import add,all,payment

urlpatterns = [
    path('add/',add,name='add invoice'),
    path('all/',all,name='add invoice'),
    path('payment/<int:id>',payment,name='add invoice'),
]