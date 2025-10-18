from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from my_books.models import *
from main_app.forms import *

# Create your views here.

def owner_login_func(request):

    

    return render(request, 'login_owner/login_owner.html')

def owner_func (request):
    totalPay = 0
    for book in Book.objects.all() :
        if book.price :
            if book.status == 'sold':
                totalPay += book.price
    
    totalRental = 0
    for book in Book.objects.all() :
        if book.total_rental :
            if book.status == 'rented':
                totalRental += book.total_rental
    
    totalsalarys = totalRental + totalPay

    context = {
        'current_time' : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
        'books'        : Book.objects.all(),
        'catigories'   : Catigory.objects.all(),
        'forms'        : new_book(),
        'add_category' : new_category(),
        'books_num'    : Book.objects.filter(active=True).count(),
        'avl_books'    : Book.objects.filter(status='availble').count(),
        'rented_books' : Book.objects.filter(status='rented').count(),
        'sold_books'  : Book.objects.filter(status='sold').count(),
        'totalsalarys' : totalsalarys,
        'totalPay'     : totalPay,
        'totalRental'  : totalRental,   
    }

    if request.method == 'POST':
        save_new_book = new_book(request.POST,request.FILES)
        if save_new_book.is_valid():
            save_new_book.save()
            return render(request, 'main_app/index.html', context)

    if request.method == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'main_app/index.html', context)

    
    return render(request, 'owner/owner.html',context)

def update_book(request,id):

    book_id = Book.objects.get(id = id)
    if request.method == 'POST':
        update_book = new_book(request.POST,request.FILES,instance = book_id)
        if update_book.is_valid():
            update_book.save()
            return redirect('/')
    else:
        update_book = new_book(instance = book_id)

    context = {
        'update_form'      : update_book,
        'selected_book'    : Book.objects.get(id = id),
    }

    return render(request,'update_book/update_book.html',context)
