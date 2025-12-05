# /home/adel101/my_work/django/LMS/LBS_venv/project/clint/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. عرض وتحديث الملف الشخصي 
    path('profile/', views.customer_profile, name='customer_profile_path'),
    
    # 2. إكمال بيانات الملف الشخصي 
    path('profile/complete/', views.complete_profile, name='complete_profile_path'),

    # 3. تسجيل الخروج 
    path('logout/', views.logout, name='logout_path'),

    #  استخدم اسم 'login' كما هو مطلوب في start.html
    path('login/', views.customer_login, name='login'),
    
    # 4. تسجيل العميل
    path('register/', views.register_user, name='register_user_path'),

]