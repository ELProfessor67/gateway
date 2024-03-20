from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse

from .filters import CustomerFilter
from transactions.forms import TransactionForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from json import dumps,loads
from .models import AllowField

def customer_list(request):

    if 'team-' in request.user.last_name:
        last_name = request.user.last_name.split('-')
        request.user.username = last_name[1]


    username = request.user.username
    customers = Customer.objects.filter(username=username)
    valid_customer = []
    for i in customers:
        i.cards = loads(i.cards)
        valid_customer.append(i)
    
    customers = valid_customer

    return render(request, 'customers/customers_list.html', {'customers': customers,'report': True,'lenght':len(customers)})

def customer_create(request):

    if 'team-' in request.user.last_name:
        last_name = request.user.last_name.split('-')
        request.user.username = last_name[1]


    if request.method == 'POST':
        print('hello world')
        authusername = request.user.username
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')
        exp_year = request.POST.get('exp_year')
        exp_month = request.POST.get('exp_month')
        cvv = request.POST.get('cvv')
        email = request.POST.get('email')
        card_number=request.POST.get('card_number')
        cards = []
        if card_number and exp_month and exp_year and cvv:
            
            new_card = {
                "card_number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvv": cvv
            }
            cards.append(new_card)
        
        cards = dumps(cards)


        Customer.objects.create(cards=cards,email=email,cvv=cvv,exp_month=exp_month,exp_year=exp_year,card_number=card_number,phone_number=phone_number,country=country,zip_code=zip_code,state=state,city=city,address=address,company=company,username=authusername,first_name=first_name,last_name=last_name)
        return redirect('/customers/customers_list/')
    form = CustomerForm()
    button_text = "Add Transaction"
    fields = AllowField.objects.filter(username=request.user.username).first()
    fields_object = {
        'first_name': True,
        'last_name': True,
        'company': True,
        'address': True,
        'city': True,
        'state': True,
        'zip_code': True,
        'country': True,
        'phone_number': True,
        'card_number': True,
        'exp_year': True,
        'exp_month': True,
        'cvv': True,
        'email': True
    }
    if fields == None:
        fields = fields_object
    return render(request, 'customers/customer_create.html', {'form': form, 'button_text': button_text,'fields': fields})

# def customer_detail(request, pk):
#     customer = get_object_or_404(Customer, pk=pk)
#     return render(request, 'customer_detail.html', {'customer': customer})

# def customer_update(request, pk):
#     customer = get_object_or_404(Customer, pk=pk)
#     if request.method == 'POST':
#         form = CustomerForm(request.POST or None, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('customers:customer_list'))
#     else:
#         form = CustomerForm(instance=customer)
#     button_text = "Update Customer"
#     return render(request, 'customers/customer_create.html', {'form': form, 'button_text': button_text})
   

# def customer_delete(request, pk):
#     customer = get_object_or_404(Customer, pk=pk)
#     if request.method == 'POST':
#         customer.delete()
#         return redirect(reverse('customers:customer_list'))
#     return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})