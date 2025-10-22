from django.urls import path
from . import views

urlpatterns = [
    # Add your URL patterns here
    path('-login', views.owner_login_func, name='owner_login_page'),
    path('update-book-<int:id>', views.update_book, name='update_book_path'),
    path('-page', views.owner_func, name='owner_page_path'),
    path('delete-book-<int:id>', views.delete, name='delete_book_path'),
    path('-page', views.owner_func, name='rented_books_path'),
    path('-rented-books', views.rented_books_func, name='rented_books_path'),
]