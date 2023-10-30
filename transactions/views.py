from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Transaction
from .forms import TransactionForm
from django.urls import reverse
from .crypto import Cryptography
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Transaction,MerchantsKey,UsersBanks
from .filters import TransactionFilter
import os
from django.contrib.auth.models import User



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from uuid import uuid1
from customers.models import Customer

import requests

import json
from json import dumps,loads
import base64
from .models import isunique
from datetime import datetime,timedelta
from django.contrib.auth import get_user_model
from django.contrib import messages
import random
import string


def generate_password():
    characters = string.ascii_letters+string.digits+string.punctuation
    password = ''.join(random.choice(characters) for i in range(15))
    return password

def get_client_ip(request):
    x_forwardef_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwardef_for:
        ip = x_forwardef_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def cutfess(amount):
    amount = int(amount)
    return (amount*2)/100

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

# for hashing transactions
KEY = 'Z_wXA1eKA99N-ddUodDW-LIgWLTsCyYWpcMjeO2vnqk='
# KEY = os.environ.get('encryption_key')

crypto = Cryptography(KEY)
payment_process_url = 'https://payment-processor.onrender.com'
# payment_process_url = 'http://localhost:4000'
secret = 'b4b94b39-7601-47c0-a7ab-39861ba9d4e3'
key = 'fb83f5f6-8141-4bc2-94a3-2b8d748ab2d4'
account = '800000'
payment_process_access_token = "27be761f-1046-49b0-be1f-35a678a41781"

@login_required(login_url='/account/login/')
def transaction_creates(request):
    if request.method == 'POST':
        
        form = TransactionForm(request.POST)

        
        if form.is_valid():
            # form.save()

            authusername = request.user.username
            transaction_id = str(uuid1())
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company = request.POST['company']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            country = request.POST['country']
            phone_number = request.POST['phone_number']
            amount = request.POST['amount']
            payment_method = request.POST['payment_method']
            transaction_type = request.POST['transaction_type']
            card_number = request.POST['card_number']
            exp_year = request.POST['exp_year']
            exp_month = request.POST['exp_month']
            cvv = request.POST['cvv']
            email = request.POST['email']
            customer = request.POST.get('customer')
            
            # print('unique',isunique(card_number,request.user.username))
            if not isunique(card_number,request.user.username):
                form = TransactionForm()
                all_customer = Customer.objects.filter(username=request.user.username).values()
                customers = {}
                for customer in all_customer:
                    del customer["date"]
                    all_cards = loads(customer.get('cards'))
                    cards = {}
                    for card in all_cards:
                        cards[card.get('card_number')] = card
                    
                    customer["cards"] = cards
                    customers[customer.get('first_name')] = customer
                customers = dumps(customers)
                button_text = "Add Transaction"
                return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text,'customers':customers,'unique':'The card you have entered is in the use of another customer please enter a valid card number'})
                        
            

            transaction = {
                "authusername": authusername,
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
                "phone_number": phone_number,
                "amount": amount,
                "payment_method": payment_method,
                "transaction_type": transaction_type,
                "card_number": card_number,
                "exp_year": exp_year,
                "exp_month": exp_month,
                "cvv": cvv,
                "email": email,
                "transaction_id": transaction_id
            }
            encrypt_transaction = crypto.encrypt(transaction)
            Transaction.objects.create(username=authusername,transaction=encrypt_transaction)


            # send to peyment processor 
            try:
                res = requests.post(f"{payment_process_url}/transation/add/?secret={secret}&key={key}&account={account}",data=transaction)
                print(res.text)
            except Exception as e:
                print(e)
            

            # customer add new card 
            customer_exist = Customer.objects.filter(first_name=first_name,email=email,last_name=last_name).first()
            if customer_exist:
                cards = loads(customer_exist.cards)
                card_exist = False
                for card in cards:
                    if card_number == card.get('card_number'):
                        card_exist = True
                
                if not card_exist:
                    new_card = {
                        "card_number": card_number,
                        "exp_month": exp_month,
                        "exp_year": exp_year,
                        "cvv": cvv
                    }

                    cards.append(new_card)
                    cards = dumps(cards)
                    customer_exist.cards = cards
                    customer_exist.save()

            
            if customer == 'on':
                cards = []
                new_card = {
                    "card_number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvv": cvv
                }

                cards.append(new_card)
                cards = dumps(cards)
                Customer.objects.create(cards=cards,email=email,cvv=cvv,exp_month=exp_month,exp_year=exp_year,card_number=card_number,phone_number=phone_number,country=country,zip_code=zip_code,state=state,city=city,address=address,company=company,username=authusername,first_name=first_name,last_name=last_name)

            return redirect('/projects/report')
    else:
        form = TransactionForm()

    all_customer = Customer.objects.filter(username=request.user.username).values()
    customers = {}
    for customer in all_customer:
        del customer["date"]
        all_cards = loads(customer.get('cards'))
        cards = {}
        for card in all_cards:
            cards[card.get('card_number')] = card
        
        customer["cards"] = cards
        customers[customer.get('first_name')] = customer
    customers = dumps(customers)
    button_text = "Add Transaction"
    return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text,'customers':customers})


users_ips_count = {}
max_limit = 5
# i add recaptcha
def getMechant(request):
        recaptcha_secret_key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
        if request.method == 'POST':
            user_ip = get_client_ip(request)
            merchant_key = request.POST.get('merchant_key')
            recaptcha_token = request.POST.get('g-recaptcha-response')

            # check recaptcha token valid aur not
            isValidToken = check_token(recaptcha_secret_key,recaptcha_token)
            if not isValidToken:
                return HttpResponse('invalid repcaptcha please try again')

            
            if user_ip in users_ips_count:
                users_ips_count[user_ip]['count'] += 1
                users_ips_count[user_ip]['last_attempt'] += datetime.now()
            else:
                users_ips_count[user_ip] = {"count":1,"last_attempt":datetime.now()}
            

            if users_ips_count[user_ip] > max_limit:
                if users_ips_count[user_ip] < datetime.now() + timedelta(minutes=60):
                    return HttpResponse('too many attempted please try again after 60 minutes')
                else:
                    users_ips_count[user_ip] = {"count":1,"last_attempt":datetime.now()}
            
            merchantUser = MerchantsKey.objects.filter(key=merchant_key).first()
            return HttpResponse(dumps(merchant_key),status=200)
        greeting = {}
        greeting['sitekey'] = recaptcha_secret_key
        return render(request,'transaction/getmerchangt.html',greeting)




@login_required(login_url='/account/login/')
def transaction_list(request):
    
    print(request.user.email)
    if 'team-' in request.user.last_name:
        last_name = request.user.last_name.split('-')
        request.user.username = last_name[1]

    # BlueSnap API endpoint for tokenization
    api_url = 'https://sandbox.bluesnap.com/services/2/payment-fields-tokens'

    # # BlueSnap API credentials
    username = 'API_16872799899141798439898'
    password = 'Findaway11!$'

    # # Credit card details
    card_number = '4111111111111111'
    expiration_month = '12'
    expiration_year = '2025'
    cvv = '123'

    # # Prepare the request payload
    payload = {
        'number': card_number,
        'expMonth': expiration_month,
        'expYear': expiration_year,
        'cvv': cvv
    }

    # # Send the request
    response = requests.post(api_url, data=json.dumps(payload), auth=(username, password))
    print("====================");
    print(response.text);
    print("<<<======================");
    # Check the response status code
    if response.status_code == 200:
        # Extract the token from the response
        token = response.json().get('paymentFieldsTokens', {}).get('paymentFieldsTokenId')
        print('Token2222222222:', token)
    else:
        # Handle the error
        print('Error:', response.text)

    if request.user.is_superuser:
        transactions = Transaction.objects.all().values()
    else:
        transactions = Transaction.objects.filter(username = request.user.username).values()
    
    for i in range(len(transactions)):
        fee = cutfess(transactions[i].get('amount'))
        transactions[i]['fee'] = fee
        transactions[i]['total'] = int(transactions[i].get('amount'))-fee

    form = TransactionForm(request.POST)
    
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
    
    print(transaction_filter)
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions,'filter': transaction_filter ,'form':form})


@csrf_exempt
@login_required(login_url='/account/login/')
def transaction_create(request):
    if 'team-' in request.user.last_name:
        last_name = request.user.last_name.split('-')
        request.user.username = last_name[1]

    if request.method == 'POST':
        
        form = TransactionForm(request.POST)

        
        if form.is_valid():
            # form.save()

            authusername = request.user.username
            transaction_id = str(uuid1())
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company = request.POST['company']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            country = request.POST['country']
            phone_number = request.POST['phone_number']
            amount = request.POST['amount']
            payment_method = request.POST['payment_method']
            transaction_type = request.POST['transaction_type']
            card_number = request.POST['card_number']
            exp_year = request.POST['exp_year']
            exp_month = request.POST['exp_month']
            cvv = request.POST['cvv']
            email = request.POST['email']
            customer = request.POST.get('customer')
            
            # print('unique',isunique(card_number,request.user.username))
            if not isunique(card_number,request.user.username):
                form = TransactionForm()
                all_customer = Customer.objects.filter(username=request.user.username).values()
                customers = {}
                for customer in all_customer:
                    del customer["date"]
                    all_cards = loads(customer.get('cards'))
                    cards = {}
                    for card in all_cards:
                        cards[card.get('card_number')] = card
                    
                    customer["cards"] = cards
                    customers[customer.get('first_name')] = customer
                customers = dumps(customers)
                button_text = "Add Transaction"
                return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text,'customers':customers,'unique':'The card you have entered is in the use of another customer please enter a valid card number'})
                        

            Transaction.objects.create(payment_method=payment_method,transaction_type=transaction_type,amount=amount,email=email,cvv=cvv,exp_month=exp_month,exp_year=exp_year,card_number=card_number,phone_number=phone_number,country=country,zip_code=zip_code,state=state,city=city,address=address,company=company,username=authusername,transaction_id=transaction_id,first_name=first_name,last_name=last_name)

            transaction = {
                "authusername": authusername,
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
                "phone_number": phone_number,
                "amount": amount,
                "payment_method": payment_method,
                "transaction_type": transaction_type,
                "card_number": card_number,
                "exp_year": exp_year,
                "exp_month": exp_month,
                "cvv": cvv,
                "email": email,
                "transaction_id": transaction_id
            }

            # encryted transactions 
            # encrypted_transaction = crypto.encrypt(dumps(transaction))
            # data = {
            #     'data': encrypted_transaction
            # }

            # send to peyment processor 
            try:
                res = requests.post(f"{payment_process_url}/transation/add/?secret={secret}&key={key}&account={account}",data=transaction)
                print(res.text)
            except Exception as e:
                print(e)
            

            # customer add new card 
            customer_exist = Customer.objects.filter(first_name=first_name,email=email,last_name=last_name).first()
            if customer_exist:
                cards = loads(customer_exist.cards)
                card_exist = False
                for card in cards:
                    if card_number == card.get('card_number'):
                        card_exist = True
                
                if not card_exist:
                    new_card = {
                        "card_number": card_number,
                        "exp_month": exp_month,
                        "exp_year": exp_year,
                        "cvv": cvv
                    }

                    cards.append(new_card)
                    cards = dumps(cards)
                    customer_exist.cards = cards
                    customer_exist.save()

            
            if customer == 'on':
                cards = []
                new_card = {
                    "card_number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvv": cvv
                }

                cards.append(new_card)
                cards = dumps(cards)
                Customer.objects.create(cards=cards,email=email,cvv=cvv,exp_month=exp_month,exp_year=exp_year,card_number=card_number,phone_number=phone_number,country=country,zip_code=zip_code,state=state,city=city,address=address,company=company,username=authusername,first_name=first_name,last_name=last_name)

            return redirect('/projects/report')
    else:
        form = TransactionForm()

    all_customer = Customer.objects.filter(username=request.user.username).values()
    customers = {}
    for customer in all_customer:
        del customer["date"]
        all_cards = loads(customer.get('cards'))
        cards = {}
        for card in all_cards:
            cards[card.get('card_number')] = card
        
        customer["cards"] = cards
        customers[customer.get('first_name')] = customer
    customers = dumps(customers)
    button_text = "Add Transaction"
    return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text,'customers':customers})


def transaction_create_ajax(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():

            # Retrieve the dynamic values from the form
            authusername = request.user.username
            transaction_id = str(uuid1())
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company = request.POST['company']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            country = request.POST['country']
            phone_number = request.POST['phone_number']
            amount = request.POST['amount']
            payment_method = request.POST['payment_method']
            transaction_type = request.POST['transaction_type']
            card_number = request.POST['card_number']
            exp_year = request.POST['exp_year']
            exp_month = request.POST['exp_month']
            cvv = request.POST['cvv']
            email = request.POST['email']
            
            



            url = "https://sandbox.bluesnap.com/services/2/transactions"


            username = 'API_16872799899141798439898'
            password = 'Findaway11!$'

            # Encode the username and password
            credentials = f'{username}:{password}'
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            print(encoded_credentials)

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Basic {encoded_credentials}',
                'bluesnap-version': '3.0',
                'Cookie': 'JSESSIONID=4DE670BDBB9367ECEC24FE4E3733CED0; TS0157275e=018b1f380ba76b438611e3dcc76ccee03c26cd38799e263e55c7722e70322357109b6f60bec79c1b4683b85c005f59f6607206e6818027fcee0fac59a8948d0e064fd37706; TS01dbdafe=018b1f380bac5d9673236c5c75a8112797c469b1ad93a48c1bfb2ccd7c0448a3a42a2c2c691f8c15f16b0e199ed3224d658c766230'
            }

            payload = {
                "amount": amount,
                "softDescriptor": "DescTest",
                "cardHolderInfo": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "zip": zip_code
                },
                "currency": "USD",
                "creditCard": {
                    "expirationYear": exp_year,
                    "securityCode": cvv,
                    "expirationMonth": exp_month,
                    "cardNumber": card_number
                },
                "cardTransactionType": "AUTH_CAPTURE"
            }
            
            transaction = {
                "authusername": authusername,
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
                "phone_number": phone_number,
                "amount": amount,
                "payment_method": payment_method,
                "transaction_type": transaction_type,
                "card_number": card_number,
                "exp_year": exp_year,
                "exp_month": exp_month,
                "cvv": cvv,
                "email": email,
                "transaction_id": transaction_id
            }

            # encryted transactions 
            encrypted_transaction = crypto.encrypt(dumps(transaction))
            data = {
                'data': encrypted_transaction
            }

            # Convert the payload to JSON string
            payload_json = json.dumps(payload)

            response = requests.post(url, headers=headers, data=payload_json)

            response_text = response.text
            print(response_text)

            response_json = json.loads(response_text)
            transaction_id = response_json.get('transactionId')

            if transaction_id is not None:
                print(f"Transaction ID: {transaction_id}")
                #token = response_json['creditCard']['token']
                #form.instance.credit_card_number = token  # Store the token in the credit_card_number field
                form.instance.transaction_id = str(transaction_id)
                # form.save()
                Transaction.objects.create(email=email,cvv=cvv,exp_month=exp_month,exp_year=exp_year,card_number=card_number,transaction_type=transaction_type,payment_method=payment_method,amount=amount,phone_number=phone_number,country=country,zip_code=zip_code,state=state,city=city,address=address,company=company,username=authusername,transaction_id=transaction_id,first_name=first_name,last_name=last_name)
                # send to peyment processor 
                res = requests.post(f"{payment_process_url}/transation/add/?token={payment_process_access_token}",data=data)
                print(res.text)
                return JsonResponse({'success': True})

            else:
                print(response_text)
                description = response_json.get('message')
                print("Transaction ID not found.")
                return JsonResponse({'success': False, 'errors': form.errors, 'message': response_text})

        else:
            return JsonResponse({'success': False, 'errors': form.errors, 'message': 'aaaa'})
    else:
        form = TransactionForm()
        button_text = "Add Transaction"



def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST or None, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect(reverse('transactions:transaction_list'))
    else:
        form = TransactionForm(instance=transaction)
    button_text = "Update Transaction"
    return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect(reverse('transactions:transaction_list'))
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})


@api_view(['POST'])

def add_api_record(request):
    token = request.data.get('token')
    if token == 'dyno@123':
        # Extract the transaction data from the request
        transaction_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'company': request.data.get('company'),
            'address': request.data.get('address', ''),  # Use default value if not provided in the request
            'city': request.data.get('city'),
            'state': request.data.get('state'),
            'zip_code': request.data.get('zip_code'),
            'country': request.data.get('country'),
            'phone_number': request.data.get('phone_number'),
            'amount': request.data.get('amount'),
            'payment_method': request.data.get('payment_method'),
            'transaction_type': request.data.get('transaction_type'),
            'card_number': request.data.get('card_number'),
            'exp_date': request.data.get('exp_date'),
            'cvv': request.data.get('cvv'),
            'email': request.data.get('email'),
        }

        # Create a new transaction record
        transaction = Transaction.objects.create(**transaction_data)

        # Return a success response
        return Response({'message': 'Transaction added successfully'})
    else:
    # Return an error response if the token is invalid
        return Response({'error': 'Invalid token'}, status=401)


shuffling_key = "hu879753426dhoehdweh_hudwhwhowi_hwdohfiowehfw_="
def limiter(request):
    req_shuf_key = request.GET.get('key')
    print(req_shuf_key)
    if req_shuf_key != shuffling_key:
        return HttpResponse('invalid swhuffling keys')
    
    users = User.objects.all()
    for user in users:
        merchant_key = MerchantsKey.objects.filter(username=user.username).first()
        if merchant_key is not None:
            shuffled_key = merchant_key.shuffling_key()
            merchant_key.key = shuffled_key
            merchant_key.save()
    return HttpResponse('all keys are shuffles')

@login_required(login_url='/')
def add_bank_account(request):
    if 'team-' in request.user.last_name:
        last_name = request.user.last_name.split('-')
        request.user.username = last_name[1]
        
    user = request.user
    account_details = UsersBanks.objects.filter(username=user.username).first()

    if request.method == "POST":
        bank_name = request.POST.get('bank_name')
        bank_address = request.POST.get('bank_address')
        account_number = request.POST.get('account_number')
        account_holder_name = request.POST.get('account_holder_name')
        account_holder_address = request.POST.get('account_holder_address')
        routing_number = request.POST.get('routing_number')
        bic_code = request.POST.get('bic_code')
        if account_details:
            account_details.bank_name = bank_name
            account_details.bank_address = bank_address
            account_details.account_holder_name = account_holder_name
            account_details.account_number = account_number
            account_details.routing_number = routing_number
            account_details.account_holder_address = account_holder_address
            account_details.bic_code = bic_code
            account_details.save()
        else:
            UsersBanks.objects.create(username=user.username,bank_name=bank_name,account_holder_name=account_holder_name,account_number=account_number,bic_code=bic_code,routing_number=routing_number,account_holder_address=account_holder_name,bank_address=bank_address)

        try:
            account_data = {
                "bank_name":  bank_name,
                "bank_address":  bank_address, 
                "account_holder_name": account_holder_name,
                "account_number": account_number,
                "routing_number": routing_number,
                "account_holder_address": account_holder_address,
                "bic_code": bic_code,
                "username": user.username
            }
            res = requests.post(f"{payment_process_url}/transation/add/bank_account/?secret={secret}&key={key}&account={account}",data=account_data)
            print(res.text)
        except Exception as e:
            print(e)

        return redirect('/transactions/add_bank_account/')
    
    greeting = {}
    greeting['btn_value'] = 'Add Account'
    greeting['heading'] = 'Add Bank Account' 
    if account_details:
        greeting['btn_value'] = 'Update Account'
        greeting['account'] = account_details
        greeting['heading'] = 'Bank Account Details' 
    
    return render(request,'transactions/add_bank_account.html',greeting)



@csrf_exempt
def my_team(request):
    user_model = get_user_model()
    # team-[owner]-[role]-[password]-[frist time]
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        user = user_model.objects.get(username=username)
        last_name = user.last_name.split('-')
        print(last_name,last_name[2])
        last_name[2] = role
        last_name = '-'.join(last_name)
        user.last_name = last_name
        user.save()
        messages.success(request,'role change successfully')
        return redirect('/transactions/my-team/')
    
    
    
    last_name = f"team-{request.user.username}"
    users = user_model.objects.filter(last_name__icontains=last_name)
    temps = []
    for i in users:
        details = i.last_name.split('-')
        i.rpassword = details[3]
        i.role = details[2]
        temps.append(i)
    
    users = temps
    return render(request,'transactions/my_team.html',{"users":users})


def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        email = request.POST.get('email')
        print(name,username,password,role)

        user_model = get_user_model()
        username_exist = user_model.objects.filter(username=username).exists()
        email_exist = user_model.objects.filter(email=email).exists()
        if username_exist:
            messages.error(request,'username already exist')
            return redirect('/transactions/add-member/')
        if email_exist:
            messages.error(request,'email already exist')
            return redirect('/transactions/add-member/')
        
        # team-[owner]-[role]-[password]-[frist time]
        last_name = f"team-{request.user.username}-{role}-{password}-True"
        print(password)
        user_model.objects.create_user(username=username,first_name=name,last_name=last_name,email=email,password=password)
        
        messages.success(request,'member add successfully.')
        return redirect('/transactions/my-team/')
    generated_pass = generate_password()
    return render(request,'transactions/add-member.html',{'password':generated_pass})