from django import forms
from .models import Laptop

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['brand', 'cpu', 'gpu', 'ram', 'storage', 'manitor', 'price', 'category', 'image']
