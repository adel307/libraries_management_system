from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def my_books(request):
    
    return render(request, 'django_template/frontend_abdelrahmanGamal/books.html')