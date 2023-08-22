import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        # fields = {
        #     'reference_number': ['exact', 'icontains'],
        #     'date': ['exact', 'gt', 'lt'],
        #     'amount': ['exact', 'gt', 'lt'],
        #     'cardholder_name': ['exact', 'icontains'],
        #     'card_type': ['exact', 'icontains'],
        #     'account': ['exact', 'icontains'],
        #     'result': ['exact', 'icontains'],
        # }
        fields = ['first_name']
