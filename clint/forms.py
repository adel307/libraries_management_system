from django import forms
from .models import Customer
import re

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'national_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم العميل الكامل'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'البريد الإلكتروني'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهاتف'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'العنوان',
                'rows': 3
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهوية الوطنية'
            }),
        }
        labels = {
            'name': 'الاسم الكامل',
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'address': 'العنوان',
            'national_id': 'رقم الهوية',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # تحقق من أن رقم الهاتف يحتوي على أرقام فقط
            if not re.match(r'^[\d\+\-\(\)\s]+$', phone):
                raise forms.ValidationError('يرجى إدخال رقم هاتف صحيح')
        return phone

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id:
            # تحقق من أن رقم الهوية يحتوي على أرقام فقط
            if not national_id.isdigit():
                raise forms.ValidationError('يجب أن يحتوي رقم الهوية على أرقام فقط')
        return national_id