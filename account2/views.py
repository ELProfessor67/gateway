from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm
)
from .forms import RegistrationForm

def account_login(request):
	if(request.method=='POST'):

		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			return redirect(reverse('projects:projects-projectslist'))
			#return render(request,'account/login.html',{'form':form})def login_view(request):
	if(request.method=='POST'):

		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			return redirect(reverse('projects:projects-projectslist'))
			#return render(request,'account/login.html',{'form':form})

	else:	
		form = AuthenticationForm()
	return render(request,'account/login.html',{'form':form})


def login_view(request):
	if(request.method=='POST'):

		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			return redirect(reverse('transactions:transaction_list'))
			#return render(request,'account/login.html',{'form':form})def login_view(request):
	if(request.method=='POST'):

		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			return redirect(reverse('transactions:transaction_list'))
			#return render(request,'account/login.html',{'form':form})

	else:	
		form = AuthenticationForm()
	return render(request,'account/login.html',{'form':form})

def signup_view(request):
	
	if request.method == 'POST':
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
		    form.save()
		    return redirect(reverse('transactions:transaction_list')) 

	else:	
		form = RegistrationForm()
	return render(request,'account/signup.html',{'form':form})

def logout_view(request):
	logout(request)
	return redirect(reverse('account:account_login'))
