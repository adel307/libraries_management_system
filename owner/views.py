from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from my_books.models import *
from main_app.forms import *
base_context = {
    'current_time' : datetime.now().strftime(f"%Y / %m / %d %H:%M:%S"),
    'catigories'   : Category.objects.all(),
    'add_category' : new_category(),
}

# Create your views here.

def owner_login_func(request):
    if request.method == 'POST':
        return redirect('owner_page_path')

    return render(request, 'login_owner.html')

def owner_func (request):
    # 2. --- Calculate Totals (Needs Optimization) ---
    # NOTE: هذه الطريقة في الحساب غير فعالة ويجب أن تعتمد على نماذج سجلات المعاملات.
    # يتم تنظيف المنطق كما هو مطلوب.
    total_pay = 0
    total_rental = 0
    
    for book in Book.objects.all():
        if book.status == 'sold' and book.price:
            total_pay += book.price
        
        if book.status == 'rented' and book.total_rental:
            total_rental += book.total_rental
            
    total_salaries = total_rental + total_pay

    filtered_books = Book.objects.exclude(status='sold')
    search = request.GET.get('search_name')
    if search:
        filtered_books = filtered_books.filter(title__icontains=search)

    if request.method == 'POST':
        
        # 1.1 معالجة نموذج إضافة كتاب جديد (يجب أن يحمل زر الإرسال name="add_book_submit")
        if 'add_book_submit' in request.POST:
            save_new_book = new_book(request.POST, request.FILES)
            if save_new_book.is_valid():
                save_new_book.save()
                messages.success(request, 'تم إضافة الكتاب بنجاح!')
            else:
                messages.error(request, 'فشل إضافة الكتاب. يرجى مراجعة البيانات.')
            return redirect('owner_page_path') # ✅ PRG Pattern
        
        # 1.2 معالجة نموذج إضافة تصنيف جديد (يجب أن يحمل زر الإرسال name="add_category_submit")
        elif 'add_category_submit' in request.POST:
            # ✅ لم تعد هناك حاجة لـ request.FILES هنا إذا كان نموذج Category يحتوي فقط على حقل الاسم
            save_new_category = new_category(request.POST) 
            if save_new_category.is_valid():
                save_new_category.save()
                messages.success(request, 'تم إضافة التصنيف بنجاح!')
            else:
                messages.error(request, 'فشل إضافة التصنيف. يرجى مراجعة البيانات.')
            return redirect('owner_page_path') # ✅ PRG Pattern

    context = {
        'forms': new_book(),
        'books': filtered_books,
        # الإحصائيات 
        'books_num': Book.objects.filter(active=True).count(),
        'sold_books': Book.objects.filter(status='sold').count(),
        'rented_books_num': Book.objects.filter(status='rented').count(),
        'avl_books': Book.objects.filter(status='available').count(),
        'AFR_books': Book.objects.filter(status='avl_for_rent').count(),
        
        # الأرباح
        'totalPay': total_pay,
        'totalRental': total_rental,
        'totalsalarys': total_salaries,
    }
    return render(request, 'owner.html',{**context , **base_context})

def update_book(request, id):
    try:
        book = get_object_or_404(Book, id=id)
        
        if request.method == 'POST':
            update_form = new_book(request.POST, request.FILES, instance=book)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'تم تحديث الكتاب بنجاح!')
            else:
                messages.error(request, 'حدث خطأ في تحديث البيانات')
        else:
            update_form = new_book(instance=book)

        context = {
            'update_form': update_form,
            'selected_book': book,
        }

        return render(request, 'update_book.html', {**context , **base_context})
        
    except Exception as e:
        messages.error(request, f'حدث خطأ: {str(e)}')
        return redirect('owner_page_path')

def delete(request,id):

    delete_book = get_object_or_404(Book,id = id)
    if request.method == 'POST':
        delete_book.delete()
        messages.success(request, f'تم حذف الكتاب "{delete_book.title}" بنجاح.') # ✅ إضافة رسالة نجاح
        return redirect('owner_page_path')
    return render(request,'delete.html',{**base_context})

def rented_books_func (request):
    filtered_books = Book.objects.filter(status = 'rented')
    search = request.GET.get('search_name')
    if search:
        filtered_books = filtered_books.filter(title__icontains=search)
    
    context = {
        'rented_books' : filtered_books,
    }
    return render(request, 'rented_books.html',{**context , **base_context})

