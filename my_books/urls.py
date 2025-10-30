from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('', views.my_books, name='my_books'),
    path('-sold-books', views.sold_books, name='sold_books_path'),
]