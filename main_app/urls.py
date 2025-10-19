from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('', views.home, name='main'),  # Example pattern
    path('description-book-<int:id>', views.description, name='description'),
    path('buy-book-<int:id>', views.buy, name='buy'),
    path('rental-book-<int:id>', views.rental, name='rental'),
    path('delete-book-<int:id>', views.delete, name='delete'),
    path('remove-book-<int:id>', views.remove, name='remove'),
]