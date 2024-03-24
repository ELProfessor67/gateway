from .models import Transaction

def transactions(request):
    # Fetch transaction data here
    transactions = Transaction.objects.filter(username = request.user.username).order_by('-date')
    return {'transactions': transactions,"transation_length": transactions.count()}