from django.urls import re_path,path
from . import views
app_name='account'
urlpatterns = [
  
    re_path(r'^login/$', views.login_view,name='account_login'),
	re_path(r'^account_reset_password/', views.login,name='account_reset_password'),
	re_path(r'^account_signup/', views.signup_view,name='account_signup'),


	re_path(r'^logout/', views.logout_view,name='logout'),    
    re_path(r'^verify-user/',views.verify,name='verify account'),
    re_path(r'^forgot-password',views.reset_password,name='forgot_password'),
    re_path(r'^reset_password/',views.forgot_password,name='reset_password'),
    # re_path(r'^account_reset_password/',views.reset_password,name='reset_password'),
    
]
