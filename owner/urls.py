from django.urls import path
from . import views

urlpatterns = [
    # Add your URL patterns here
    path('', views.owner_func, name='owner_path'),  # Example pattern
]