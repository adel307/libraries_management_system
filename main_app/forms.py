from django import forms
from my_books.models import *

class new_book (forms.ModelForm):
    class Meta :
        model = Book
        fields = [
            'title',
            'auther',
            'book_image',
            'auther_image',
            'price',
            'status',
            'pages',
            'active',
            'retal_price_day',
            'retal_proid',
            'catigery',
            'total_rental',
            'discription',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'auther': forms.TextInput(attrs={'class':'form-control'}),
            'book_image': forms.FileInput(attrs={'class':'form-control'}),
            'auther_image': forms.FileInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'pages': forms.NumberInput(attrs={'class':'form-control'}),
            'active': forms.TextInput(attrs={'class':'form-control'}),
            'retal_price_day': forms.NumberInput(attrs={'class':'form-control','id':'RetalPriceDay'}),
            'retal_proid': forms.NumberInput(attrs={'class':'form-control','id':'RetalProid'}),
            'total_rental': forms.NumberInput(attrs={'class':'form-control','id':'TotalRental'}),
            'catigery': forms.Select(attrs={'class':'form-control'}),
            'discription': forms.TextInput(attrs={'class':'form-control'}),
        }


class new_category (forms.ModelForm):
    class Meta :
        model = Category
        fields = [
            'name',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }
