from django.urls import path
from .views import add,all

urlpatterns = [
    path('add/',add,name='add invoice'),
    path('all/',all,name='add invoice'),
]