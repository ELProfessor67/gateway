from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout
from transactions.models import ApproveMails
import requests
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm
)
from .forms import RegistrationForm
from django.contrib import messages

def check_token(recaptcha_secret_key,recaptcha_token):
    data = {
        'secret':recaptcha_secret_key,
        'response':recaptcha_token
    }
    res = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
    result = res.json()
    if result['success']:
        return True
    else:
        return False
	
recaptcha_secret_key = "6LeBXZooAAAAAHchFf5EBPFgyUBLI-bCSFv8VjQ0"
recaptcha_site_key = "6LeBXZooAAAAAIHbtqWafsINysZ5MZk8fWvpfODb"


# def account_login(request):
# 	if(request.method=='POST'):

# 		recaptcha_token = request.POST.get('g-recaptcha-response')
# 		isValidToken = check_token(recaptcha_secret_key,recaptcha_token)
# 		if not isValidToken:
# 			return HttpResponse('invalid repcaptcha please try again')
	
# 		form = AuthenticationForm(data=request.POST)		
# 		if form.is_valid():
# 			user = form.get_user()
# 			login(request,user)
# 			return redirect('/%2Faccount/dashboard2')
# 			#return render(request,'account/login.html',{'form':form})def login_view(request):
# 	# if(request.method=='POST'):

# 	# 	form = AuthenticationForm(data=request.POST)
# 	# 	if form.is_valid():
# 	# 		user = form.get_user()
# 	# 		login(request,user)
# 			# return redirect(reverse('projects:projects-projectslist'))
# 			#return render(request,'account/login.html',{'form':form})

# 	else:	
# 		form = AuthenticationForm()
# 	return render(request,'account/login.html',{'form':form})


def login_view(request):
	if(request.method=='POST'):
		recaptcha_token = request.POST.get('g-recaptcha-response')
		isValidToken = check_token(recaptcha_secret_key,recaptcha_token)

		if not isValidToken:
			messages.error(request,'Invalid recaptcha')
			return redirect('/')
		
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			# return redirect(reverse('transactions:transaction_list'))
			return redirect('/%2Faccount/dashboard2')
			#return render(request,'account/login.html',{'form':form})def login_view(request):
	# if(request.method=='POST'):

	# 	form = AuthenticationForm(data=request.POST)
	# 	if form.is_valid():
	# 		user = form.get_user()
	# 		login(request,user)
	# 		return redirect(reverse('transactions:transaction_list'))
			#return render(request,'account/login.html',{'form':form})

	else:	
		form = AuthenticationForm()
	return render(request,'account/login.html',{'form':form,'recaptcha_site_key':recaptcha_site_key})

def signup_view(request):
	form = RegistrationForm()

	if request.method == 'POST':
		form = RegistrationForm(data=request.POST)
		email = request.POST.get('email')
		
		email_approval_list = ApproveMails.objects.filter(email=email).first()

		if email_approval_list == None:
			return render(request,'account/signup.html',{'form':form,"error_message": "notapply"})
		
		if email_approval_list.status == 'disapprove':
			return render(request,'account/signup.html',{'form':form,"error_message": "disapproved"})

		if form.is_valid():
		    form.save()
		    return redirect(reverse('transactions:transaction_list'))
		
		else:
			form = RegistrationForm()
	return render(request,'account/signup.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect(reverse('account:account_login'))
