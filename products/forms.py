# forms.py

from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'quantity', 'price', 'image', 'category', 'discountDeadline')


class DateInput(forms.DateInput):
    input_type = 'date'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'quantity', 'price', 'discount', 'discountStatus', 'discountDeadline', 'image')
        widgets = {
            'discountDeadline': DateInput()
        }
