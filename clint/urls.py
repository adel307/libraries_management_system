# /home/adel101/my_work/django/LMS/LBS_venv/project/clint/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. عرض وتحديث الملف الشخصي (تم إزالة الشرطة المائلة الأمامية)
    path('profile/', views.customer_profile, name='customer_profile_path'),
    
    # 2. إكمال البيانات (باستخدام الدالة المحسّنة complete_profile)
    path('profile/complete/', views.complete_profile, name='complete_profile_path'),

    # 3. تسجيل الخروج (باستخدام الدالة الآمنة user_logout)
    # يجب عليك التأكد من أن دالة views.logout تم تغيير اسمها إلى views.user_logout
    path('logout/', views.user_logout, name='logout_path'),

    #  استخدم اسم 'login' كما هو مطلوب في start.html
    path('login/', views.customer_login, name='login'), 
    
    # 4. حذف رابط تسجيل العميل (register_customer) إذا كان يستخدم لإنشاء عميل غير موجود.
    # إذا كنت ما زلت بحاجة لرابط تسجيل المستخدم الأساسي، يجب أن يكون في مكان آخر (مثل app التسجيل الرئيسي).
]