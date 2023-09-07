from django.http import request
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse_lazy
from transactions.models import Transaction
from datetime import datetime, timedelta, date
from json import dumps
from collections import defaultdict
from math import trunc

def get_card_transaction_lengths(transactions):
    card_transaction_lengths = defaultdict(int)

    for transaction in transactions:
        company = transaction.get_card_company()
        card_transaction_lengths[company] += 1

    return dict(card_transaction_lengths)



# utillity
class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Dashboard"
        greeting['pageview'] = "Dashboards"
        username = request.user.username
        dateinput = request.GET.get('date')
        
        if (dateinput is None):
            dateinput = datetime.now()
        else:
            year,month,day = dateinput.split('-')
            dateinput = datetime(int(year), int(month), int(day),0,0,0)
            dateinput = dateinput + timedelta(hours=13)
        
        void_transactions = Transaction.objects.filter(username=username,date__date=dateinput).exclude(transaction_type = 'refund').values()
        total = sum([int(transaction.get('amount')) for transaction in void_transactions])
        greeting['total'] = total
        if len(void_transactions) == 0:
            greeting['avg'] = 0
        else:
            greeting['avg'] = trunc(total/len(void_transactions))
        
        refund_transactions = Transaction.objects.filter(transaction_type = 'refund',username=username,date__date = dateinput).values()

        refund = sum([int(transaction.get('amount')) for transaction in refund_transactions])
        
        # login for line chart data
        end_date = dateinput
        start_date = end_date - timedelta(days=6)
        chart_transactions = Transaction.objects.filter(date__range=(start_date, end_date),username=username)
        today = dateinput
        today_index = today.weekday()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create the desired list starting from today
        week_list = [days_of_week[(today_index + i) % 7] for i in range(7)]
        first_element = week_list.pop(0)
        week_list.append(first_element)

        transactions_by_day = {
        }

        for i in week_list:
            transactions_by_day[i] = []
        
        transactions_by_day['week_list'] = week_list



        for transaction in chart_transactions:
            day_of_week = transaction.date.strftime('%A')
            transactions_by_day[day_of_week].append({
                'id': transaction.id,
                'amount': transaction.amount,  # Replace 'amount' with the actual field name
                # Add other transaction fields you want to include
            })
        

        # logic fot dougnut graph
        all_transactions = Transaction.objects.filter(date__date=dateinput,username=username)
        card_transaction_lengths = get_card_transaction_lengths(all_transactions)

        greeting['chart_transaction'] = dumps(transactions_by_day)
        greeting['doughnut_data'] = dumps(card_transaction_lengths)
        greeting['refund'] = refund
        greeting['orders'] = len(void_transactions) + len(refund_transactions)
        return render(request, 'dashboard/dashboard.html',greeting)


class SaasView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "Saas"
        greeting['pageview'] = "Dashboards"
        return render (request,'dashboard/dashboard-saas.html',greeting)

class CryptoView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "Crypto" 
        greeting['pageview'] = "Dashboards"
        return render (request,'dashboard/dashboard-crypto.html',greeting)

class BlogView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "Blog" 
        greeting['pageview'] = "Dashboards"
        return render (request,'dashboard/dashboard-blog.html',greeting)

class JobsView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "Jobs" 
        greeting['pageview'] = "Dashboards"
        return render (request,'dashboard/dashboard-jobs.html',greeting)        

class CalendarView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "TUI Calendar"
        greeting['pageview'] = "Calendars"
        return render (request, 'calendar.html',greeting)
class CalendarFullView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Full Calendar"
        greeting['pageview'] = "Calendars"
        return render (request, 'calendar-full.html',greeting)
class ChatView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Chat"
        greeting['pageview'] = "Apps"
        return render (request, 'chat-view.html',greeting)

class FileManagerView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "File Manager"
        greeting['pageview'] = "Apps"
        return render (request,'filemanager.html',greeting)

# Authentication
class PagesLoginView(View):
    def get(self, request):
        return render(request, 'authentication/pages-login.html')
class PagesRegisterView(View):
    def get(self, request):
        return render(request, 'authentication/pages-register.html')
class PagesRecoverpwView(View):
    def get(self, request):
        return render(request, 'authentication/pages-recoverpw.html')
class PagesLockscreenView(View):
    def get(self, request):
        return render(request, 'authentication/pages-lockscreen.html')

class PagesConfirmmailView(View):
    def get(self, request):
        return render(request, 'authentication/pages-confirmmail.html')

class PagesEmailVerificationView(View):
    def get(self, request):
        return render(request, 'authentication/pages-emailverificationmail.html')

class PagesTwoStepVerificationView(View):
    def get(self, request):
        return render(request, 'authentication/pages-twostepverificationmail.html')
class PagesLogin2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-login-2.html')
class PagesRegister2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-register-2.html')
class PagesRecoverpw2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-recoverpw2.html')
class PagesLockscreen2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-lockscreen2.html')

class PagesConfirmmail2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-confirmmail-2.html')

class PagesEmailVerification2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-emailverificationmail-2.html')

class PagesTwoStepVerification2View(View):
    def get(self, request):
        return render(request, 'authentication/pages-twostepverificationmail-2.html')

class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('dashboard')
class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('dashboard')

