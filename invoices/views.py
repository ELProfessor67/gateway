from django.shortcuts import render,redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Invoices
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/")
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        Invoices.objects.create(
            name=name,
            email=email,
            amount=amount,
            phone=phone,
            address=address,
            status='pending',  # default status
            created_at=timezone.now(),
            owner=request.user
        )
        return redirect('/invoices/all')
    return render(request,"invoices/addInvoice.html") 



@login_required(login_url="/")
def all(request):
    invocies = Invoices.objects.filter(owner=request.user)
    return render(request,"invoices/all.html",{"invoices": invocies}) 



@login_required(login_url="/")
def payment(request,id):
    invoice = Invoices.objects.get(pk=id)
    if request.method == 'POST':
        invoice.status = "paid"
        invoice.save()
        return HttpResponse("Paid Successfully")
    return render(request,"invoices/payment.html",{"invoice":invoice}) 