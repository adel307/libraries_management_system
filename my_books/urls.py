from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('', views.my_books, name='books'),  # Example pattern
]