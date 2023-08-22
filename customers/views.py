from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse

from .filters import CustomerFilter

from rest_framework.decorators import api_view
from rest_framework.response import Response


def customer_list(request):
    customers = Customer.objects.all()
    
    customer_filter = CustomerFilter(request.GET, queryset=Customer.objects.all())

    return render(request, 'customers/customers_list.html', {'customers': customers,'filter': customer_filter})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('customers:customer_list'))
    else:
        form = CustomerForm()
    button_text = "Add Transaction"
    return render(request, 'customers/customer_create.html', {'form': form, 'button_text': button_text})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_detail.html', {'customer': customer})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST or None, instance=customer)
        if form.is_valid():
            form.save()
            return redirect(reverse('customers:customer_list'))
    else:
        form = CustomerForm(instance=customer)
    button_text = "Update Customer"
    return render(request, 'customers/customer_create.html', {'form': form, 'button_text': button_text})
   

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect(reverse('customers:customer_list'))
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})