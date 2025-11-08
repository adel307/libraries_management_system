from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from my_books.models import *
from main_app.forms import *

# Create your views here.

def owner_login_func(request):

    

    return render(request, 'login_owner.html')

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
        'books'            : Book.objects.all(),
        'books_num'        : Book.objects.filter(active=True).count(),
        'sold_books'       : Book.objects.filter(status='sold').count(),
        'rented_books_num' : Book.objects.filter(status='rented').count(),
        'avl_books'        : Book.objects.filter(status='available').count(),
        'AFR_books'        : Book.objects.filter(status='avl_for_rent').count(),
        'current_time'     : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
        'catigories'       : Category.objects.all(),
        'forms'            : new_book(),
        'add_category'     : new_category(),
        'totalPay'         : totalPay,
        'totalRental'      : totalRental,   
        'totalsalarys'     : totalsalarys,
    }

    if request.method == 'POST':
        save_new_book = new_book(request.POST,request.FILES)
        if save_new_book.is_valid():
            save_new_book.save()
            return render(request, 'index.html', context)

    if request.method == 'POST':
        save_new_category = new_category(request.POST,request.FILES)
        if save_new_category.is_valid():
            save_new_category.save()
            return render(request, 'index.html', context)

    
    return render(request, 'owner.html',context)

def update_book(request, id):
    try:
        book = get_object_or_404(Book, id=id)
        
        if request.method == 'POST':
            update_form = new_book(request.POST, request.FILES, instance=book)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'تم تحديث الكتاب بنجاح!')
                return redirect('owner_page_path')
            else:
                messages.error(request, 'حدث خطأ في تحديث البيانات')
        else:
            update_form = new_book(instance=book)

        context = {
            'update_form': update_form,
            'selected_book': book,
        }

        return render(request, 'update_book.html', context)
        
    except Exception as e:
        messages.error(request, f'حدث خطأ: {str(e)}')
        return redirect('owner_page_path')

def delete(request,id):

    delete_book = get_object_or_404(Book,id = id)
    if request.method == 'POST':
        delete_book.delete()
        return redirect('/')
    return render(request,'delete.html')

def rented_books_func (request):
    search = None
    search_value = Book.objects.all()
    if 'search_name' in request.GET:
        search = request.GET['search_name']
        if search:
            search_value = search_value.filter(title__icontains = search)
    
    context = {
        'rented_books' : Book.objects.filter(status = 'rented'),
        'catigories' : Category.objects.all(),
        'add_category' : new_category(),
    }

    
    

    return render(request, 'rented_books.html',context)

