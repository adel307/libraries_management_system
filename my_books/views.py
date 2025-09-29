from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import *

def my_books(request):
    
    context = {
        'books' : Book.objects.all()
    }
    return render(request, 'django_template/frontend_abdelrahmanGamal/books.html',context)