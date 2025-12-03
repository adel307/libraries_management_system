from django.urls import path
from . import views

urlpatterns = [
    # 1. صفحة تسجيل دخول المالك
    path('-login', views.owner_login_func, name='owner_login_page'),
    
    # 2. لوحة تحكم المالك الرئيسية (مسار فريد)
    path('-page', views.owner_func, name='owner_page_path'),
    
    # 3. تحديث كتاب
    path('update-book-<int:id>', views.update_book, name='update_book_path'),
    
    # 4. حذف كتاب
    path('delete-book-<int:id>', views.delete, name='delete_book_path'),
    
    # 5. عرض الكتب المستأجرة (مسار واسم فريد)
    path('-rented-books', views.rented_books_func, name='rented_books_path'),
]