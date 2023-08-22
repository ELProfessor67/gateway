from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    transaction_id = forms.CharField(
        label='Transaction ID',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='11'
    )
    class Meta:
        model = Transaction
        fields = [
            'first_name',
            'last_name',
            'company',
            'address',
            'city',
            'state',
            'zip_code',
            'country',
            'phone_number',
            'amount',
            'payment_method',
            'transaction_type',
            'card_number',
            'exp_year',
            'exp_month',
            'cvv',
            'email',
            'transaction_id'  # Corrected field name to lowercase 'transaction_id'
        ]
        
        widgets = {
            'amount': forms.Textarea(attrs={'rows': 1, 'cols': 30}),
            'payment_method': forms.RadioSelect(choices=[('credit', 'Credit Card'), ('check', 'Check')]),
            'transaction_type': forms.Select(choices=[('change1', 'Change 1'), ('change2', 'Change 2')]),
        }

    def clean_card_number(self):
        self.fields['card_number'].errors = {'invalid': 'Card number must be 16 digits.'}
        card_number = self.cleaned_data['card_number']
        
        if len(card_number) != 16:
            raise forms.ValidationError("Card number must be 16 digits.")

        return card_number

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data.get('transaction_id')
        
        if transaction_id:
            # Perform any specific validation for transaction_id here if needed
            pass

        return transaction_id

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.pop('transaction_id', None)  # Remove transaction_id from cleaned_data
        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card_number'].errors = {'invalid': 'Card number must be 16 digits.'}
