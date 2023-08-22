import django_filters
from .models import Customer

class CustomerFilter(django_filters.FilterSet):
	#custom_filter = django_filters.CharFilter(method='filter_custom_field')

	def filter_custom_field(self, queryset, name, value):
	    # Custom filter logic for a custom_field
	    # ...
	    print("==")

	class Meta:
	    model = Customer
	    fields = {
	        #'customer_id': ['exact'],
	        # 'bill_company': ['exact', 'icontains'],
	        # 'bill_first_name': ['exact', 'icontains'],
	        # 'bill_last_name': ['exact', 'icontains'],
	        # 'recurring_schedule': ['exact'],
	        # 'bill_phone_number': ['exact', 'icontains'],
	        # 'email': ['exact', 'icontains'],
	    }
	    fields = ['customer_id']
