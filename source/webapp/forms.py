from decimal import Decimal
from django import forms
from webapp.models import Category


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Наименование')
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control', 'rows': 3}), label='Описание')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='-- Выберите категорию --', label='Категория',
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    price = forms.DecimalField(max_digits=7, decimal_places=2, min_value=Decimal('0.01'), label='Стоимость', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(min_value=0, label='Остаток', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.URLField(max_length=1000, label='Изображение', widget=forms.URLInput(attrs={'class': 'form-control'}))

class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Search by name'}))