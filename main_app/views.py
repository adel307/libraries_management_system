from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from my_books.models import *
from .forms import *                                                                                          



def home(request):

    context = {
        'current_time' : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
        'books'        : Book.objects.all(),
        'catigories'   : Catigory.objects.all(),
        'forms'        : new_book(),
        'add_category' : new_category()
    }

    if request.method == 'POST':
        save_new_book = new_book(request.POST,request.FILES)
        if save_new_book.is_valid():
            save_new_book.save()
            return render(request, 'django_template/frontend_abdelrahmanGamal/index.html', context)

    if request.method == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'django_template/frontend_abdelrahmanGamal/index.html', context)

    
    return render(request, 'django_template/frontend_abdelrahmanGamal/index.html', context)    

def update(request,id):

    book_id = Book.objects.get(id = id)
    if request.method == 'POST':
        update_book = new_book(request.POST,request.FILES,instance = book_id)
        if update_book.is_valid():
            update_book.save()
            return redirect('/')
    else:
        update_book = new_book(instance = book_id)

    context = {
        'update_form' : update_book,
    }

    return render(request,'django_template/frontend_abdelrahmanGamal/update.html',context)

def delete(request,id):

    delete_book = get_object_or_404(Book,id = id)
    if request.method == 'POST':
        delete_book.delete()
        return redirect('/')
    return render(request,'django_template/frontend_abdelrahmanGamal/delete.html')

