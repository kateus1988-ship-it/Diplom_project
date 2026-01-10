from django import forms
from cars.models import Car, DealRequest

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('owner',)

class DealRequestForm(forms.ModelForm):
    class Meta:
        model = DealRequest
        exclude = ('seeker', 'car', 'status', 'date_approved')