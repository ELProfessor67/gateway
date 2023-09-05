from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse

from .filters import CustomerFilter
from transactions.forms import TransactionForm

from rest_framework.decorators import api_view
from rest_framework.response import Response


def customer_list(request):
    username = request.user.username
    customers = Customer.objects.filter(username=username)

    return render(request, 'customers/customers_list.html', {'customers': customers,'report': True})

def customer_create(request):
    if request.method == 'POST':
        print('hello world')
        authusername = request.user.username
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        company = request.POST['company']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        country = request.POST['country']
        phone_number = request.POST['phone_number']
        exp_year = request.POST['exp_year']
        exp_month = request.POST['exp_month']
        cvv = request.POST['cvv']
        email = request.POST['email']
        card_number=request.POST['card_number']

        Customer.objects.create(email=email,cvv=cvv,exp_month=exp_month,exp_year=exp_year,card_number=card_number,phone_number=phone_number,country=country,zip_code=zip_code,state=state,city=city,address=address,company=company,username=authusername,first_name=first_name,last_name=last_name)
        return redirect('/customers/customers_list/')
    form = CustomerForm()
    button_text = "Add Transaction"
    return render(request, 'customers/customer_create.html', {'form': form, 'button_text': button_text})

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