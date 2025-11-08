from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from clint.models import Customer, CustomerBook
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from my_books.models import *
from .forms import *
from clint.models import *
base_context = {
    'current_time' : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
    'catigories'   : Category.objects.all(),
    'add_category' : new_category(),
}

def home(request):
    if Customer.objects.filter(user_id = request.user.id).first():
        context = {
            'forms'            : new_book(),
            'books'            : Book.objects.exclude(status='sold'),
            'books_num'        : Book.objects.filter(active=True).count(),
            'sold_books'       : Book.objects.filter(status='sold').count(),
            'rented_books_num' : Book.objects.filter(status='rented').count(),
            'avl_books'        : Book.objects.filter(status='available').count(),
            'customer'         : Customer.objects.filter(user_id = request.user.id).first(),
        }

        if request.method == 'POST':
            save_new_book = new_book(request.POST,request.FILES)
            if save_new_book.is_valid():
                save_new_book.save()
                return render(request, 'index.html', {**context , **base_context})

        if request.method == 'POST':
            save_new_category = new_category(request.POST,request.FILES)
            if save_new_category.is_valid():
                save_new_category.save()
                return render(request, 'index.html', {**context , **base_context})

        return render(request, 'index.html', {**context , **base_context})
    else:
        return render(request, 'start.html')

def description(request,id):
    book_id = Book.objects.get(id = id)
    context = {
        'description_form' : description_book,
        'selected_book'    : Book.objects.get(id = id),
    }

    if request.method == 'POST':
        description_book = new_book(request.POST,request.FILES,instance = book_id)
        if description_book.is_valid():
            description_book.save()
            return redirect('/')
    else:
        description_book = new_book(instance = book_id)

    return render(request,'description.html',{**context , **base_context})

def remove(request,id):
    book = get_object_or_404(Book,id = id)
    context = {
        'customer' : Customer.objects.filter(user_id = request.user.id).first(),
    }

    if request.method == 'POST':
        try:
            if book.status == 'sold':
                book.status = 'available'
                book.save()
                messages.success(request, f' تم حذف الكتاب  "{book.title}" من قائمة كتبك! ')
            return redirect('main')
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'حدث خطأ أثناء عملية الحدف')
            return redirect('main')

    return render(request,'remove.html',{**context , **base_context})

def buy(request, id):
    book = get_object_or_404(Book, id=id)
    context = {
        'selected_book': book,
        'customer' : Customer.objects.filter(user_id = request.user.id).first(),
    }
    
    if request.method == 'POST':
        try:
            if book.status == 'available':
                book.status = 'sold'
                book.save()

                try:
                    customer = Customer.objects.filter(user_id = request.user.id).first()
                except Customer.DoesNotExist:
                    messages.error(request, 'لم يتم العثور على بيانات العميل!')
                    return redirect('main')

                # إضافة الكتاب إلى Customer books مع تجنب التكرار
                customer_book, created = CustomerBook.objects.get_or_create(
                    customer=customer,
                    book=book,
                    defaults={'purchase_price': book.price}  # سعر الشراء الافتراضي
                )
                
                messages.success(request, f'تم شراء الكتاب "{book.title}" بنجاح!')
            else:
                messages.warning(request, 'هذا الكتاب غير متاح للشراء!')
                
            return redirect('customer_profile_path')
            
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'حدث خطأ أثناء عملية الشراء')
            return redirect('main')
    
    return render(request, 'buy.html', {**context , **base_context})

def rental(request, id):
    book = get_object_or_404(Book, id=id)
    context = {
        'selected_book': book,
    }

    if request.method == 'POST':
        try:
            if book.status == 'avl_for_rent':
                book.status = 'rented'
                book.save()
                
                messages.success(request, f'تم استئجار الكتاب "{book.title}" بنجاح!')
            else:
                messages.warning(request, 'هذا الكتاب غير متاح للإيجار !')
                
            return redirect('main')
            
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'حدث خطأ أثناء عملية للإيجار')
            return redirect('main')
    
    return render(request, 'rental.html', context)