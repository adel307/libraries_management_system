from django.urls import path
from . import views

urlpatterns = [
    path('/customer_profile', views.customer_profile, name='customer_profile_path'),
    #path('/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
]