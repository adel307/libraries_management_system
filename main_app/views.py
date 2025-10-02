from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from my_books.models import *
from .forms import *                                                                                          



def home(request):
    if request.method == 'POST':
        save_new_book = new_book(request.POST,request.FILES)
        if save_new_book.is_valid():
            save_new_book.save()

    if request.method == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()

    context = {
        'current_time' : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
        'books'        : Book.objects.all(),
        'catigories'   : Catigory.objects.all(),
        'forms'        : new_book(),
        'add_category' : new_category()
    }
    return render(request, 'django_template/frontend_abdelrahmanGamal/index.html', context)

def update(request):
    
    return render(request,'django_template/frontend_abdelrahmanGamal/update.html')