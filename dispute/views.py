
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dispute
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/")
def add(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        type = request.POST.get('type')

        Dispute.objects.create(
            description=description,
            type=type,
            created_at=timezone.now(),
            owner=request.user
        )
        return redirect('/dispute/all')
    return render(request,"dispute/add.html") 



@login_required(login_url="/")
def all(request):
    disputes=None
    if(request.user.is_superuser):
        disputes = Dispute.objects.all()
    else:
        disputes = Dispute.objects.filter(owner=request.user)
    return render(request,"dispute/all.html",{"disputes":disputes}) 
