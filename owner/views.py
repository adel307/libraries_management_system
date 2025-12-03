from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
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
    # حساب إجمالي المبيعات
    total_pay = Book.objects.filter(status='sold').aggregate(Sum('price'))['price__sum'] or 0

    # حساب إجمالي الإيجارات
    total_rental = Book.objects.filter(status='rented').aggregate(Sum('total_rental'))['total_rental__sum'] or 0

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
            # 1. إنشاء النموذج من بيانات POST (يحتوي على الأخطاء المحتملة)
            update_form = new_book(request.POST, request.FILES, instance=book)

            if update_form.is_valid():
                update_form.save()
                messages.success(request, f'تم تحديث الكتاب "{book.title}" بنجاح!')
                return redirect('owner_page_path')
            else:
                # 2. عند الفشل: يتم تعيين رسالة الخطأ والسماح للكود بالمرور إلى return render
                messages.error(request, 'حدث خطأ في تحديث البيانات. يرجى مراجعة الحقول المشار إليها بالأخطاء.')
        else:
            # 3. في حالة GET: إنشاء النموذج بالبيانات الحالية
            update_form = new_book(instance=book)

        # 4. يتم تمرير النموذج (الناجح، أو الفاشل والمحمل بالأخطاء) إلى context
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

