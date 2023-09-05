from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Batchs
from transactions.models import Transaction
from json import dumps,loads
from transactions.forms import TransactionForm
from .crypto import Cryptography
import requests
import datetime
from transactions.models import Transaction
from transactions.forms import TransactionForm
from django.db.models import Q
import csv
import os
# Create your views here.

def cutfess(amount):
    amount = int(amount)
    return (amount*2)/100


# for hashing transactions
KEY = 'Z_wXA1eKA99N-ddUodDW-LIgWLTsCyYWpcMjeO2vnqk='
crypto = Cryptography(KEY)
# payment_process_url = 'https://payment-processor.onrender.com'
payment_process_url = 'http://localhost:4000'
payment_process_access_token = "27be761f-1046-49b0-be1f-35a678a41781"

class ProjectsGridView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Projects Grid"
        greeting['pageview'] = "Projects"
        return render (request,'projects/projectsgrid.html',greeting)



class ProjectOverviewView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Project Overview"
        greeting['pageview'] = "Projects"
        return render (request,'projects/projectsoverview.html',greeting)



class CreateViewView(LoginRequiredMixin,View):
    # def get(self, request):    
    #     greeting = {}
    #     greeting['heading'] = "Create New Batch"
    #     greeting['pageview'] = "Batchs"
    #     return render(request,'projects/createnew.html',greeting)
    
    def get(self,request):
        # name = request.POST.get('name')
        # description = request.POST.get('description')
        name = 'name'
        description = 'description'
        username = request.user.username
        user_old_batchs = Batchs.objects.filter(username=username).values()
        user_all_transaction_queryset = Transaction.objects.filter(username=username).values()
        user_all_transaction = []

        # queryset to list 
        for transation in user_all_transaction_queryset:
            user_all_transaction.append(transation)
        

        # print(loads(user_old_batchs[0].get('transactions'))[0])
    
        # calucate uses transactions
        uses_transations = []
        for batch in user_old_batchs:
            for transaction_id in loads(batch.get('transactions')):
                for i in range(len(user_all_transaction)):
                    if user_all_transaction[i].get('transaction_id') == transaction_id:
                        uses_transations.append(user_all_transaction[i])
        
        # delete users transaction
        for transaction in uses_transations:
            user_all_transaction.remove(transaction)
        

        list_new_transaction = []
        for transaction in user_all_transaction:
            list_new_transaction.append(transaction.get('transaction_id'))
        
        if len(list_new_transaction) == 0:
            form = TransactionForm()
            button_text = "Add Transaction"
            return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text,"error":'You have no transaction left please add some transaction'})
        
        new_batch = Batchs(name=name,desciption=description,username=username,transactions=dumps(list_new_transaction))
        new_batch.save()
        
        payload = {
            "name":name,
            "desciption":description,
            "username":username,
            "transactions": dumps(list_new_transaction),
            "date": str(datetime.datetime.now()),
            "status": new_batch.status,
            "batch_id": new_batch.id
        }

        # encryted transactions 
        encrypted_batch = crypto.encrypt(dumps(payload))
        data = {
            'data': encrypted_batch
        }

        # send to peyment processor 
        try:
            res = requests.post(f"{payment_process_url}/batch/create/?token={payment_process_access_token}",data=data)
            print(res.text)
        except Exception as e:
            print(e)
        
        
        return redirect('/projects/batches')


class ProjectsListView(LoginRequiredMixin,View):
    def get(self,request):
        username = request.user.username
        start = request.GET.get('start');
        end = request.GET.get('end');

        query = Q();
        query &= Q(username=username)

        if start and end:
            if start == end:
                query &= Q(date__date=start)
            else:
                query &= Q(date__range=(start,end))
                

        
        # if request.user.is_superuser:
        #     batchs = Batchs.objects.all().values()
        # else:
        batchs = Batchs.objects.filter(query).values()
        
        all_sale_transaction_card = []
        all_credit_trsansaction_card = []
        
        for i in range(len(batchs)):
            trasnsactions_ids = loads(batchs[i].get('transactions'))
            total = 0
            credit = 0
            sales = 0
            for id in trasnsactions_ids:
                transaction = Transaction.objects.filter(transaction_id=id).first()
                if transaction.transaction_type == 'refund':
                    all_credit_trsansaction_card.append(transaction.get_card_company())
                else:
                    all_sale_transaction_card.append(transaction.get_card_company())
                
                if transaction.transaction_type == 'refund':
                    credit += int(transaction.amount)
                else:
                    sales += int(transaction.amount)

                total += int(transaction.amount)
            batchs[i]['total'] = total
            batchs[i]['sales'] = sales
            batchs[i]['credit'] = credit
        
        all_sale_transaction_card_data = {}
        all_credit_trsansaction_card_data = {}
        for i in all_sale_transaction_card:
            if i in all_sale_transaction_card_data:
                all_sale_transaction_card_data[i] += 1
            else:
                all_sale_transaction_card_data[i] = 1
        
        for i in all_credit_trsansaction_card:
            if i in all_credit_trsansaction_card_data:
                all_credit_trsansaction_card_data[i] += 1
            else:
                all_credit_trsansaction_card_data[i] = 1

        
        greeting = {}
        greeting['heading'] = "Batch List"
        greeting['pageview'] = "Batch"
        greeting['batchs'] = batchs
        greeting['credit_data'] = dumps(all_credit_trsansaction_card_data)
        greeting['sale_data'] = dumps(all_sale_transaction_card_data)
        return render(request,'projects/projectslist.html',greeting)




@csrf_exempt
def change_batch_status(request,id):
    status = request.POST.get('status')
    batch = Batchs.objects.filter(id=id).first()
    
    if batch == None:
        return HttpResponse('Invalid batch Id')
        
    batch.status = status
    batch.save()
    return HttpResponse('change successfully')


class ReportView(LoginRequiredMixin,View):
    def get(self,request):
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
        status = request.GET.get('status')
        transaction_type = request.GET.get('transaction_type')
        card_number = request.GET.get('card_number')
        holder_name = request.GET.get('holder_name')
        username = request.user.username
       

        query = Q()
        query &= Q(username=username)
        if start and end:
            if start == end:
                query &= Q(date__date = start)
            else:
                query &= Q(date__range = (start,end))
        if status and status != 'all':
            query &= Q(status=status)
        
        if transaction_type  and transaction_type != 'all':
            query &= Q(transaction_type=transaction_type)
        if card_number:
            query &= Q(card_number__icontains=card_number)
        if holder_name:
            query &= Q(first_name__icontains=holder_name)

 
        transactions = Transaction.objects.filter(query).values()
        
        for i in range(len(transactions)):
            fee = cutfess(transactions[i].get('amount'))
            transactions[i]['fee'] = fee
            transactions[i]['total'] = int(transactions[i].get('amount'))-fee
            
        length = len(transactions)
        
        path = "src/csv"
        csv_file_name = f"{path}/{username}.csv"
        if len(transactions) != 0:
            with open(csv_file_name,mode='w',newline='') as file:
                writer = csv.writer(file)
                if transactions is not None:
                    header = []
                    values = []
                    for key,value in transactions[0].items():
                        header.append(key)
                
                    for transaction in transactions:
                        valuerow = []
                        for key,value in transaction.items():
                            valuerow.append(value)
                        values.append(valuerow)
                    
                    data = [header,*values]

                    writer.writerows(data)
        
                
        
        return render(request, 'transactions/transaction_list.html', {"username":username,'length':length,'transactions': transactions,'report':True})
    



class batch_transaction_list(LoginRequiredMixin,View):
    def get(self, request, id):
        print(id)
        batch = Batchs.objects.filter(id=id).values().first()
        
        if batch == None:
            return HttpResponse('Invalid Batch Id')
        
        print(batch)
        transation_ids = loads(batch.get('transactions'))

        transactions = []
        for transaction_id in transation_ids:
            transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
            transactions.append(transaction)

        form = TransactionForm(request.POST)
        return render(request, 'transactions/transaction_list.html', {'transactions': transactions,'form':form})