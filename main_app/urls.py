from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('', views.home, name='main'),  # Example pattern
    path('update-book-<int:id>', views.update, name='update'),
    path('delete-book-<int:id>', views.delete, name='delete'),
]