from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages
from django.contrib.auth import login, authenticate , logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from my_books.models import Category
from .models import Customer
from .forms import CustomerForm

@login_required
def customer_profile(request):
    """عرض الملف الشخصي للعميل"""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        # إذا لم يكن هناك ملف عميل، أنشئ واحداً
        customer = Customer.objects.create(user=request.user)
        messages.info(request, 'تم إنشاء ملفك الشخصي تلقائياً')
    
    context = {
        'customer': customer,
        'catigories' : Category.objects.all(),
    }
    return render(request, 'clint/customer_profile.html', context)

def complete_profile(request):
    """
    إكمال بيانات الملف الشخصي للعميل
    """
    # 1. جلب كائن العميل أو إنشاؤه (شبكة أمان)
    # ملاحظة: الإشارة (Signal) يجب أن تكون قد أنشأته بالفعل
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        # إنشاء ملف عميل إذا لم يكن موجوداً
        customer = Customer.objects.create(user=request.user)
        messages.info(request, 'تم إنشاء ملفك الشخصي تلقائياً.')
    
    if request.method == 'POST':
        # 2. إنشاء نموذج (Form) باستخدام البيانات المرسلة (POST) والملفات (FILES)
        # وتمرير كائن العميل الحالي (instance) للتحديث
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        
        if form.is_valid():
            # 3. حفظ البيانات المتحقق من صحتها وتحديث كائن العميل
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('customer_profile')
        else:
            # عرض رسالة خطأ عامة بالإضافة إلى أخطاء النموذج
            messages.error(request, 'يرجى تصحيح الأخطاء المشار إليها في النموذج.')
    else:
        # 4. إذا كان الطلب GET، اعرض النموذج مملوءاً بالبيانات الحالية للعميل
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'clint/complete_profile.html', context)

def register_user(request):
    """تسجيل مستخدم جديد في نموذج User"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                # حفظ المستخدم الجديد
                user = form.save()
                
                # تسجيل الدخول تلقائياً
                login(request, user)
                
                messages.success(request, f'تم إنشاء حسابك بنجاح! مرحباً {user.username}')
                return redirect('main')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إنشاء الحساب: {str(e)}')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = UserCreationForm()
    
    return render(request, 'clint/register.html', {'form': form})


# def customer_list(request):
#     customers = Customer.objects.all().order_by('-created_at')
#     context = {
#         'customers': customers,
#         'title': 'قائمة العملاء'
#     }
#     return render(request, 'clint/customer_list.html', context)

# @login_required
# def update_customer(request, id):
#     customer = get_object_or_404(Customer, id=id)
    
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, f'تم تحديث بيانات العميل {customer.name} بنجاح!')
#                 return redirect('customer_list')  # أو أي صفحة تريد
#             except Exception as e:
#                 messages.error(request, f'حدث خطأ أثناء التحديث: {str(e)}')
#         else:
#             messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
#     else:
#         form = CustomerForm(instance=customer)
    
#     context = {
#         'form': form,
#         'title': 'تعديل بيانات العميل',
#         'customer': customer
#     }
#     return render(request, 'clint/customer_form.html', context)

# def edit_customer(request, customer_id):
#     """تعديل بيانات العميل"""
#     customer = get_object_or_404(Customer, id=customer_id)
    
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'تم تحديث بيانات العميل بنجاح')
#             return redirect('customer_profile', customer_id=customer.id)
#     else:
#         form = CustomerForm(instance=customer)
    
#     return render(request, 'edit_customer.html', {
#         'form': form,
#         'customer': customer,
#     })
def user_logout(request):
    """
    تسجيل خروج المستخدم بشكل آمن (إنهاء الجلسة) دون حذف بياناته.
    """

    if request.method == 'POST':
        # 1. استخدام دالة auth_logout لإنهاء الجلسة وحذف كوكيز التسجيل
        auth_logout(request) 
        
        # 2. إرسال رسالة نجاح
        messages.success(request, 'تم تسجيل خروجك بنجاح من النظام.')
        
        # 3. التوجيه إلى الصفحة الرئيسية
        return redirect('main')
    
    # في حال كان الطلب GET، اعرض صفحة التأكيد على تسجيل الخروج
    # (يفضل تغيير اسم القالب في نظامك ليصبح clint/logout_confirm.html أو ما شابه)
    return render(request, 'logout.html')