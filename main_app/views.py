from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from clint.models import *
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
        
        filtered_books = Book.objects.exclude(status='sold')
        search = request.GET.get('search_name')
        if search:
            filtered_books = filtered_books.filter(title__icontains=search)

        context = {
            'forms'            : new_book(),
            'books'            : filtered_books,
            'books_num'        : Book.objects.filter(active=True).count(),
            'sold_books'       : Book.objects.filter(status='sold').count(),
            'rented_books_num' : Book.objects.filter(status='rented').count(),
            'avl_books'        : Book.objects.filter(status='available').count(),
            'customer'         : Customer.objects.filter(user_id = request.user.id).first(),
        }
        return render(request, 'index.html', {**context , **base_context})
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
    return render(request,'description.html',{**context , **base_context})

def remove(request, id):
    # 1. جلب الكائن أو إظهار خطأ 404 إذا لم يتم العثور عليه
    book = get_object_or_404(Book, id=id)

    # 2. التحقق من أن الطلب هو POST
    if request.method == 'POST':
        try:
            # 3. حذف الكتاب نهائياً من قاعدة البيانات
            book_title = book.title  # حفظ العنوان قبل الحذف
            book.delete()
            
            # 4. إظهار رسالة نجاح
            messages.success(request, f' تم حذف الكتاب "{book_title}" نهائياً من قواعد البيانات. ')
            
            # 5. إعادة التوجيه إلى الصفحة الرئيسية
            return redirect('main')
            
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'حدث خطأ أثناء عملية الحذف النهائي.')
            return redirect('main')

    # 6. معالجة طلب GET (لإظهار صفحة التأكيد)
    context = {
        'book_to_remove': book, # نمرر الكتاب لعرض تفاصيله في القالب
        'customer': Customer.objects.filter(user_id=request.user.id).first(),
    }
    # يجب أن يعرض القالب 'remove.html' زر تأكيد POST للحذف
    return render(request, 'remove.html', {**context, **base_context})

def buy(request, id):
    book = get_object_or_404(Book, id=id)
    
    if request.method == 'POST':
        try:
            customer = Customer.objects.filter(user_id = request.user.id).first()
            try:
                if book.status == 'available':
                    book.status = 'sold'
                    book.save()

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
        except Customer.DoesNotExist:
            messages.error(request, 'لم يتم العثور على بيانات العميل!')
            return redirect('main')

    context = {
        'selected_book': book,
        'customer' : Customer.objects.filter(user_id = request.user.id).first(),
    }
    return render(request, 'buy.html', {**context , **base_context})

def rental(request, id):
    book = get_object_or_404(Book, id=id)
    
    if request.method == 'POST':
        try:
            customer = Customer.objects.filter(user_id = request.user.id).first()
            try:
                if book.status == 'avl_for_rent':
                    book.status = 'rented'
                    book.save()

                    # إضافة الكتاب إلى Customer Rented Book مع تجنب التكرار
                    customer_book, created = CustomerRentedBook.objects.get_or_create(
                        customer=customer,
                        book=book,
                        defaults={'purchase_price': book.total_rental}
                    )
                    
                    messages.success(request, f'تم استئجار الكتاب "{book.title}" بنجاح!')
                else:
                    messages.warning(request, 'هذا الكتاب غير متاح للاستئجار!')
                    
                return redirect('customer_profile_path')
                
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, 'حدث خطأ أثناء عملية الاستئجار')
                return redirect('main')
        except Customer.DoesNotExist:
            messages.error(request, 'لم يتم العثور على بيانات العميل!')
            return redirect('main')

    context = {
        'selected_book': book,
        'customer' : Customer.objects.filter(user_id = request.user.id).first(),
    }
    return render(request, 'buy.html', {**context , **base_context})