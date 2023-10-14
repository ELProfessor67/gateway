from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Batchs, Shedules
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
from django.contrib.auth.models import User
import os
import requests
from django.contrib.auth.decorators import login_required
# Create your views here.

def cutfess(amount):
    amount = int(amount)
    return (amount*2)/100


# for hashing transactions
KEY = 'Z_wXA1eKA99N-ddUodDW-LIgWLTsCyYWpcMjeO2vnqk='
crypto = Cryptography(KEY)
payment_process_url = 'https://payment-processor.onrender.com'
# payment_process_url = 'http://localhost:4000'
secret = 'b4b94b39-7601-47c0-a7ab-39861ba9d4e3'
key = 'fb83f5f6-8141-4bc2-94a3-2b8d748ab2d4'
account = '800000'
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



class CreateViewView(View):
    # def get(self, request):    
    #     greeting = {}
    #     greeting['heading'] = "Create New Batch"
    #     greeting['pageview'] = "Batchs"
    #     return render(request,'projects/createnew.html',greeting)
    
    def get(self,request):
        # name = request.POST.get('name')
        # description = request.POST.get('description')
        userkey = request.GET.get('key')

        if userkey != KEY:
            return HttpResponse('invalid key')
        
        users = User.objects.all()
        for user in users:
            
            name = 'name'
            description = 'description'
            username = user.username
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
            
            if len(list_new_transaction) != 0:
                # form = TransactionForm()
                # button_text = "Add Transaction"
                # return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text,"error":'You have no transaction left please add some transaction'})
            
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
                # encrypted_batch = crypto.encrypt(dumps(payload))
                # data = {
                #     'data': encrypted_batch
                # }

                # send to peyment processor s
                try:
                    res = requests.post(f"{payment_process_url}/batch/create/?secret={secret}&key={key}&account={account}",data=payload)
                    print(res.text)
                except Exception as e:
                    print(e)
            
            
        # return redirect('/projects/batches')
        return HttpResponse('all batch create successfully')


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

        
        path = "src/csv"
        csv_file_name = f"{path}/{username}.csv"
        if len(batchs) != 0:
            with open(csv_file_name,mode='w',newline='') as file:
                writer = csv.writer(file)
                if batchs is not None:
                    header = []
                    values = []
                    for key,value in batchs[0].items():
                        if key != 'transactions':
                            header.append(key)
                
                    for batch in batchs:
                        valuerow = []
                        for key,value in batch.items():
                            if key != 'transactions':
                                valuerow.append(value)
                        values.append(valuerow)
                    
                    data = [header,*values]

                    writer.writerows(data)


        greeting = {}
        greeting['heading'] = "Batch List"
        greeting['pageview'] = "Batch"
        greeting['batchs'] = batchs
        greeting['credit_data'] = dumps(all_credit_trsansaction_card_data)
        greeting['sale_data'] = dumps(all_sale_transaction_card_data)
        greeting['username'] = username
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
                print('calliing')
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
        else:
            open(csv_file_name,'w+')

        
                
        
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




# get refund 
@login_required(login_url='/')
def get_credit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        refundData = {
            "amount": amount,
            "username": request.user.username
        }
        res = requests.post(f"{payment_process_url}/get/refund/?secret={secret}&key={key}&account={account}",data=refundData)
        if res.status_code == 200:
            Batchs.objects.create(username=request.user.username,amount=amount)
        
        result = res.json()

        return HttpResponse(request,result.message)

    encrypted_transction = Transaction.objects.filter(username=request.user.username)
    transaction = []
    for i in encrypted_transction:
        decrypt = crypto.decrypt(i.transaction)
        if decrypt.transaction_type == 'refund':
            transaction.append(decrypt)
    
    total_refund = sum([int(i.amount) for i in transaction])
    greeting = {}
    greeting['total_refund'] = total_refund
    return render(request,'projects/get_credit.html',greeting)
    







class create_shedule(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'projects/create_shedule.html')

    def post(self,request):
        form_data = request.POST
        custom = form_data.get('custom')
        email = form_data.get('email')
        username = request.user.username
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        company = form_data.get('company')
        address = form_data.get('address')
        city = form_data.get('city')
        state = form_data.get('state')
        zip_code = form_data.get('zip_code')
        country =   form_data.get('country')
        phone_number = form_data.get('phone_number')

        # payments fields 
        payment_name = form_data.get('payment_name')
        card_number = form_data.get('card_number')
        exp_year = form_data.get('exp_year')
        exp_month = form_data.get('exp_month')
        cvv = form_data.get('cvv')

        # recustion feilds
        name = form_data.get('name')
        description = form_data.get('description')
        amount = form_data.get('amount')
        every = form_data.get('every')
        gap = form_data.get('gap')
        start = form_data.get('start')
        end = form_data.get('end')
        after = form_data.get('after')
        afterwith = form_data.get('afterwith')

        schedule = Shedules.objects.create(custom=custom,email=email,username=username,first_name=first_name,last_name=last_name,company=company,address=address,city=city,state=state,zip_code=zip_code,country=country,phone_number=phone_number,payment_name=payment_name,card_number=card_number,exp_year=exp_year,exp_month=exp_month,cvv=cvv,name=name,description=description,amount=amount,every=every,gap=gap,start=start,end=end,after=after,afterwith=afterwith)

        
        return redirect('/projects/recurring_list')



class shedule_list(LoginRequiredMixin,View):
    def get(self,request):
        username = request.user.username
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        query = Q()
        query &= Q(username=username)
        if start and end:
            if start == end:
                query &= Q(date__date=start)
            else:
                query &= Q(date__range=(start,end))
        schedules = Shedules.objects.filter(query)
        return render(request,'projects/schedules_list.html',{'schedules':schedules})