
from django.urls import path
from .views import add, all, single_product, order_product,chechout,all_orders

urlpatterns = [
    path('add/',add,name="add Items"),
    path('all/',all,name="all Items"),
    path('products/<int:id>',single_product,name="single product"),
    path('checkout/<int:id>',chechout,name="chechout"),
    path('order/<int:id>',order_product,name="order"),
    path('orders/',all_orders,name="all order")
]