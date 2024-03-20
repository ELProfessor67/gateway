from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
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
from projects.models import OTP_Object, Token_Object
import random
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
import os
import hashlib
import base64

def generateOTP():
	otp = random.randint(100000,999999)
	return otp


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
			
			# login(request,user)
			otp = generateOTP()
			user_exist = OTP_Object.objects.filter(username=user.username).first()
			if user_exist:
				user_exist.otp = otp
				user_exist.created_at = datetime.datetime.now()
				user_exist.attempt = 0
				user_exist.save()
			else:
				OTP_Object.objects.create(username=user.username,otp=otp)
			
			# send otp 
			subject = 'Trifection.com user verification'
			message = f"your varification otp is {otp}"
			from_mail = settings.EMAIL_HOST_USER
			email = user.email
			to = [email]
			send_mail(subject,message,from_mail,to,fail_silently=False)
			print(otp)
			
			# return redirect('/%2Faccount/dashboard2')
			messages.info(request,email[0:4])
			return redirect('/account/verify-user')

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


def verify(request):
	if request.method == "POST":
		otp1 = request.POST.get("1")
		otp2 = request.POST.get("2")
		otp3 = request.POST.get("3")
		otp4 = request.POST.get("4")
		otp5 = request.POST.get("5")
		otp6 = request.POST.get("6")
		email = request.POST.get("email")

		otp = otp1+otp2+otp3+otp4+otp5+otp6
		otp_deatils = OTP_Object.objects.filter(otp=otp).first()
		if otp_deatils:
			print(otp_deatils.username)
			user_model = get_user_model()
			user = user_model.objects.get(username=otp_deatils.username)
			user.backend = "django.contrib.auth.backends.ModelBackend"
			# print(user.password)
			login(request,user)

			last_name = user.last_name
			if 'team-' in last_name:
				first_time = last_name.split('-')[4]
				if first_time == 'True':
					last_name = last_name.split('-')
					last_name[4] = 'False'
					user.last_name = '-'.join(last_name)
					user.save()
					messages.info(request,'please change password')
					return redirect('/change-password')
				
			return redirect('/%2Faccount/dashboard2')
		else:
			messages.error(request,'Invalif OTP')
			messages.info(request,email)
			return redirect('/account/verify-user')

	return render(request,'account/verification_sent.html')




def forgot_password(request):
	print(request)
	if request.method == "POST":
		email = request.POST.get('email')

		random_bytes = os.urandom(20)
		# random_bytes = str(base64.b64encode(random_bytes).decode('utf-8'))
		# print(random_bytes)
		hashed_bytes = hashlib.sha256(random_bytes).hexdigest()

		user_model = get_user_model()
		user = user_model.objects.filter(email=email).first()
		if user == None:
			return render(request, 'account/reset_passwoes.html', {"message": f"No User Exist"})

		user_exist = Token_Object.objects.filter(username=user.username).first()
		print(str(hashed_bytes))
		if user_exist:                                                
			user_exist.reset_token = str(hashed_bytes)
			user_exist.created_at = datetime.datetime.now()
			user_exist.save()
		else:
			Token_Object.objects.create(username=user.username,reset_token=str(hashed_bytes))


		subject = 'Trifection.com reset password link'
		referer = request.META.get('HTTP_ORIGIN')
		url = f"{referer}/account/forgot-password?token={hashed_bytes}"
		print(url)
		message = f"your reset link is {url}"
		from_mail = settings.EMAIL_HOST_USER
		email = user.email
		to = [email]
		send_mail(subject,message,from_mail,to,fail_silently=False)
		return render(request, 'account/reset_passwoes.html', {"message": f"Reset link sent to your email {email}"})
	return render(request,'account/reset_passwoes.html')




def reset_password(request):
	if request.method == "POST":
		token = request.GET.get("token")
		password = request.POST.get('password')
		cpassword = request.POST.get('cpassword')

		if(cpassword != password):
			return render(request,'account/forgot_password.html',{"message": "password and confirm password does not match"})

		token_details = Token_Object.objects.filter(reset_token=token).first()
		if token_details:
			user_model = get_user_model()
			user = user_model.objects.get(username=token_details.username)
			user.set_password(password)
			user.save()
			token_details.reset_token = ""
			token_details.save()

				
			return render(request,'account/forgot_password.html',{"message": "password reset successfully"})
		else:
			return render(request,'account/forgot_password.html',{"message": "Invalid Reset Token"})
		print(token_deatils)
	return render(request,'account/forgot_password.html')