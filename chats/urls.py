from django.urls import path
from .views import customerService, getAnswer


urlpatterns = [
    path("customer-service/",customerService,name="customer service"),
    path("answer/",getAnswer,name="get answer"),
]