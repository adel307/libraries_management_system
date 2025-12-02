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
            # 1. تنظيف الرقم: إزالة كل ما هو ليس رقمًا أو علامة + (لكود الدولة)
            # ركز على استخراج الأرقام وعلامة +
            cleaned_phone = re.sub(r'[^\d\+]', '', phone)
            
            # إزالة علامة + إذا لم تكن في البداية لتجنب حالات مثل 123+456
            if '+' in cleaned_phone[1:]:
                raise forms.ValidationError('علامة الزائد (+) مسموح بها فقط في بداية رقم الهاتف.')
                
            # إزالة علامة + للتحقق من الطول
            digits_only = cleaned_phone.replace('+', '')
            
            # 2. التحقق من الطول (يجب أن يكون بين 7 و 15 رقمًا بعد إزالة كود الدولة)
            # هذا نطاق مرن يغطي معظم الأرقام الدولية
            if len(digits_only) < 7 or len(digits_only) > 15:
                raise forms.ValidationError('يجب أن يحتوي رقم الهاتف على ما بين 7 و 15 رقمًا.')
            
            # 3. التحقق من أن ما تبقى هو أرقام فقط (بعد إزالة +)
            if not digits_only.isdigit():
                 # (من الناحية الفنية هذا لن يحدث بعد re.sub ولكن هو تحذير منطقي)
                 raise forms.ValidationError('رقم الهاتف يحتوي على حروف غير مسموح بها.')

            # إرجاع الرقم النظيف لضمان تخزين تنسيق موحد في قاعدة البيانات (مثل +97150xxxxxxx)
            return cleaned_phone
            
        return phone

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id:
            # 💡 التعديل: الاكتفاء بالتحقق من أن الحقل يحتوي على أرقام فقط (0-9).
            # ملاحظة: إذا كانت بعض الهويات قد تحتوي على أحرف لاتينية، يجب استخدام r'^\w+$' بدلاً من isdigit().
            # ولكن للهوية الوطنية، الأرقام هي القاعدة.
            if not national_id.isdigit():
                raise forms.ValidationError('يجب أن يحتوي رقم الهوية على أرقام فقط.')
                
            # ✅ تم إزالة التحقق من الطول الثابت (مثل len(national_id) != 14) ليتناسب مع الهويات الدولية.
                 
        return national_id