from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import *
from main_app.forms import new_category


def my_books(request):

    search = None
    search_value = Book.objects.all()
    if 'search_name' in request.GET:
        search = request.GET['search_name']
        if search:
            search_value = search_value.filter(title__icontains = search)
    
    if 'cat_filter' in request.GET:
        print(1)


    context = {
        'books' : search_value,
        'catigories'  : Catigory.objects.all(),
        'add_category' : new_category()
    }

    if request.method  == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'my_book/books.html',context)
    if 'horror-category' in request.GET:
        print(True)

    return render(request, 'my_book/books.html',context)    

