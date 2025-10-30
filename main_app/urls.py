from django.urls import path
from . import views  
from clint.models import Customer

urlpatterns = [
    # Add your URL patterns here
    
    path('', views.home, name='main'),
    path('description-book-<int:id>', views.description, name='description'),
    path('buy-book-<int:id>', views.buy, name='buy'),
    path('rental-book-<int:id>', views.rental, name='rental'),
    path('remove-book-<int:id>', views.remove, name='remove'),
]