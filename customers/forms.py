from django import forms
from .models import Customer
class CustomerForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Custom validation logic for the email field
        # ...
        return email

    class Meta:
        model = Customer
        fields = ['customer_id', 'bill_company', 'bill_first_name', 'bill_last_name', 'recurring_schedule', 'bill_phone_number', 'email']
        # Additional form field customization
        widgets = {
            'recurring_schedule': forms.Select(attrs={'class': 'custom-select'} , choices=[('change1', 'Change 1'), ('change2', 'Change 2')]),
            'bill_phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        }
