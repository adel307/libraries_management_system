from django.urls import path
from . import views

urlpatterns = [
    path('/customer-profile', views.customer_profile, name='customer_profile_path'),
    path('customer-register/', views.register_customer, name='register_customer'),
    path('customer-logout/', views.logout, name='logout_path'),
    # path('customer/update/<int:id>/', views.update_customer, name='update_customer'),
    #path('/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
]