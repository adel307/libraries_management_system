from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from clint.models import Customer
from .models import *
from main_app.forms import new_category


def my_books(request):

    search = None
    search_value = Book.objects.all()
    if 'search_name' in request.GET:
        search = request.GET['search_name']
        if search:
            search_value = search_value.filter(title__icontains = search)
    
    customer = get_object_or_404(Customer)

    context = {
        'books' : search_value,
        'catigories'  : Category.objects.all(),
        'add_category' : new_category(),
        'customer': customer,
    }

    if request.method  == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'user_books.html',context)
    

    return render(request, 'user_books.html',context)

def sold_books(request):

    search = None
    search_value = Book.objects.all()
    if 'search_name' in request.GET:
        search = request.GET['search_name']
        if search:
            search_value = search_value.filter(title__icontains = search)
    
    customer = get_object_or_404(Customer)

    context = {
        'books' : search_value,
        'catigories'  : Category.objects.all(),
        'add_category' : new_category(),
        'customer': customer,
    }

    if request.method  == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'owner_books.html',context)
    

    return render(request, 'owner_books.html',context)

