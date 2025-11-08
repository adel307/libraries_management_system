from django.shortcuts import render, get_object_or_404, redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from my_books.models import Category
from .models import Customer
from .forms import CustomerForm

def customer_profile(request):
    """عرض بيانات العميل"""
    customer = Customer.objects.filter(user_id = request.user.id).first()
    context ={
        'customer': customer,
        'catigories' : Category.objects.all(),
    }
    return render(request, 'customer_profile.html',context)

def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                customer = form.save(commit=False)
                customer.user_id = request.user.id
                customer.save()
                
                messages.success(request, f'تم تسجيل العميل {customer.name} بنجاح!')
                return redirect('main')
                
            except Exception as e:
                print("خطأ في الحفظ:", str(e))  
                messages.error(request, f'حدث خطأ أثناء التسجيل: {str(e)}')
        else:
            print("=== أخطاء النموذج ===")
            print("الأخطاء:", form.errors)
            print("البيانات غير الصالحة:", form.non_field_errors())
            
            
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request, f'{field_name}: {error}')
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'تسجيل عميل جديد'
    }
    return render(request, 'signup.html', context)

# def customer_list(request):
#     customers = Customer.objects.all().order_by('-created_at')
#     context = {
#         'customers': customers,
#         'title': 'قائمة العملاء'
#     }
#     return render(request, 'clint/customer_list.html', context)

# @login_required
# def update_customer(request, id):
#     customer = get_object_or_404(Customer, id=id)
    
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, f'تم تحديث بيانات العميل {customer.name} بنجاح!')
#                 return redirect('customer_list')  # أو أي صفحة تريد
#             except Exception as e:
#                 messages.error(request, f'حدث خطأ أثناء التحديث: {str(e)}')
#         else:
#             messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
#     else:
#         form = CustomerForm(instance=customer)
    
#     context = {
#         'form': form,
#         'title': 'تعديل بيانات العميل',
#         'customer': customer
#     }
#     return render(request, 'clint/customer_form.html', context)

# def edit_customer(request, customer_id):
#     """تعديل بيانات العميل"""
#     customer = get_object_or_404(Customer, id=customer_id)
    
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'تم تحديث بيانات العميل بنجاح')
#             return redirect('customer_profile', customer_id=customer.id)
#     else:
#         form = CustomerForm(instance=customer)
    
#     return render(request, 'edit_customer.html', {
#         'form': form,
#         'customer': customer,
#     })
def logout (request):
    customer = Customer.objects.filter(user_id = request.user.id).first()
    if request.method == 'POST': 
        customer.delete()
        return redirect('main')
    return render(request,'logout.html')
