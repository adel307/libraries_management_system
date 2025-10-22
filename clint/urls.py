from django.urls import path
from . import views

urlpatterns = [
    path('customer/<int:customer_id>/', views.customer_profile, name='customer_profile'),
    path('customer/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    # ... الروابط الأخرى
]