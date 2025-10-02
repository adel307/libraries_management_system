from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import *
from main_app.forms import new_category


def my_books(request):

    if request.method  == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            
            
    
    context = {
        'books' : Book.objects.all(),
        'catigories'  : Catigory.objects.all(),
        'add_category' : new_category()
    }
    return render(request, 'django_template/frontend_abdelrahmanGamal/books.html',context)