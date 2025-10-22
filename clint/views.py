from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm

def customer_profile(request, customer_id):
    """عرض بيانات العميل"""
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customer_profile.html', {'customer': customer})

def edit_customer(request, customer_id):
    """تعديل بيانات العميل"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث بيانات العميل بنجاح')
            return redirect('customer_profile', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'edit_customer.html', {
        'form': form,
        'customer': customer
    })