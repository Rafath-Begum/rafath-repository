from django import forms
from .models import Address

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class CheckoutForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none(), required=False)
    full_name = forms.CharField(max_length=200, required=False)
    street = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    zipcode = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=30, required=False)
    note = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["address"].queryset = user.addresses.all()