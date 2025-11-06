from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from clint.models import Customer, CustomerBook
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from my_books.models import *
from .forms import *
from clint.models import *





def home(request):
    if Customer.objects.exists():
        totalPay = 0
        for book in Book.objects.all() :
            if book.price :
                if book.status == 'sold':
                    totalPay += book.price

        totalRented = 0
        for book in Book.objects.all() :
            if book.total_rental :
                if book.status == 'rented':
                    totalRented += book.total_rental

        totalsalarys = totalRented + totalPay

        context = {
            'current_time' : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
            'books' : Book.objects.exclude(status='sold'),
            'catigories' : Category.objects.all(),
            'forms' : new_book(),
            'add_category' : new_category(),
            'books_num' : Book.objects.filter(active=True).count(),
            'avl_books' : Book.objects.filter(status='available').count(),
            'rented_books_num' : Book.objects.filter(status='rented').count(),
            'sold_books' : Book.objects.filter(status='sold').count(),
            'totalsalarys' : totalsalarys,
            'totalPay' : totalPay,
            'totalRented' : totalRented,
            'clint_id': request.user.id if request.user.is_authenticated else None,
            'customer': Customer.objects.filter(user_id = request.user.id).first(),
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

        return render(request, 'index.html', context)
    else:
        return render(request, 'start.html')

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

    return render(request,'description.html',context)


def remove(request,id):

    book = get_object_or_404(Book,id = id)

    if request.method == 'POST':

        try:
            # التحقق من أن الكتاب لم يباع بالفعل
            if book.status == 'sold':
                # تغيير حالة الكتاب إلى sold
                book.status = 'available'
                book.save()
                 
  
 
                messages.success(request, f' تم حذف الكتاب  "{book.title}" من قائمة كتبك! ')
            
                
            return redirect('main')
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'حدث خطأ أثناء عملية الحدف')
            return redirect('main')
    return render(request,'remove.html')

def buy(request, id):
    # الحصول على الكتاب
    book = get_object_or_404(Book, id=id)
    
    if request.method == 'POST':
        try:
            # التحقق من أن الكتاب لم يباع بالفعل
            if book.status == 'available':
                # تغيير حالة الكتاب إلى sold
                book.status = 'sold'
                book.save()

                # الحصول على العميل المرتبط بالمستخدم الحالي
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
                messages.warning(request, 'هذا الكتاب مباع بالفعل!')
                
            return redirect('customer_profile_path')
            
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'حدث خطأ أثناء عملية الشراء')
            return redirect('main')
    
    # إذا كان الطلب GET، اعرض صفحة الشراء
    context = {
        'selected_book': book,
    }
    return render(request, 'buy.html', context)

def rental(request, id):
    # الحصول على الكتاب
    book = get_object_or_404(Book, id=id)
    
    if request.method == 'POST':
        try:
            # التحقق من أن الكتاب لم يباع بالفعل
            if book.status == 'avl_for_rent':
                # تغيير حالة الكتاب إلى sold
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
    
    # إذا كان الطلب GET، اعرض صفحة الشراء
    context = {
        'selected_book': book,
    }
    return render(request, 'rental.html', context)