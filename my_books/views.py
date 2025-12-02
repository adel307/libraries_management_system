from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from clint.models import Customer
from .models import *
from main_app.forms import new_category


def my_books(request):
    
    """عرض كتب المستخدم"""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    filtered_books = customer.my_books.all()
    search = request.GET.get('search_name')
    if search:
        filtered_books = filtered_books.filter(title__icontains=search)

    context = {
        'books': filtered_books,
        'catigories': Category.objects.all(),
        'add_category': new_category(),
        'customer': customer,
        'search_query': search,
    }
    return render(request, 'user_books.html', context)

def sold_books(request):

    filtered_books = Book.objects.filter(status='sold')
    search = request.GET.get('search_name')
    if search:
        filtered_books = filtered_books.filter(title__icontains=search)
    
    customer = get_object_or_404(Customer)

    if request.method  == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'owner_books.html',context)
    
    context = {
        'books' : filtered_books,
        'catigories'  : Category.objects.all(),
        'add_category' : new_category(),
        'customer': customer,
    }
    return render(request, 'owner_books.html',context)

