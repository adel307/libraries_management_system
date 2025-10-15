from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from my_books.models import *
from .forms import *                                                                                          



def home(request):

    

    totalPay = 0
    for book in Book.objects.all() :
        if book.price :
            if book.status == 'solid':
                totalPay += book.price
    
    totalRental = 0
    for book in Book.objects.all() :
        if book.total_rental :
            if book.status == 'rental':
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
        'rental_books' : Book.objects.filter(status='rental').count(),
        'solid_books'  : Book.objects.filter(status='solid').count(),
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

    
    return render(request, 'main_app/index.html', context)    

def description(request,id):

    book_id = Book.objects.get(id = id)
    if request.method == 'POST':
        description_book = new_book(request.POST,request.FILES,instance = book_id)
        if description_book.is_valid():
            description_book.save()
            return redirect('/')
    else:
        description_book = new_book(instance = book_id)

    context = {
        'description_form' : description_book,
        'selected_book'    : Book.objects.get(id = id),
    }

    return render(request,'main_app/description.html',context)

def delete(request,id):

    delete_book = get_object_or_404(Book,id = id)
    if request.method == 'POST':
        delete_book.delete()
        return redirect('/')
    return render(request,'main_app/delete.html')

