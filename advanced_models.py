from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import os
from datetime import timedelta

class Category(models.Model):
    """نموذج التصنيفات"""
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف", unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Author(models.Model):
    """نموذج المؤلفين"""
    name = models.CharField(max_length=100, verbose_name="اسم المؤلف")
    bio = models.TextField(blank=True, null=True, verbose_name="السيرة الذاتية")
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name="الجنسية")
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")
    
    class Meta:
        verbose_name = "مؤلف"
        verbose_name_plural = "المؤلفون"
        ordering = ['name']
    
    def __str__(self):
        return self.name

def book_image_path(instance, filename):
    """تحديد مسار حفظ صورة الكتاب"""
    ext = filename.split('.')[-1]
    filename = f"book_{instance.id}_{instance.title}.{ext}"
    return os.path.join('books/images/', filename)

def book_file_path(instance, filename):
    """تحديد مسار حفظ ملف الكتاب"""
    ext = filename.split('.')[-1]
    filename = f"book_{instance.id}_{instance.title}.{ext}"
    return os.path.join('books/files/', filename)

class Book(models.Model):
    """نموذج الكتب"""
    
    STATUS_CHOICES = [
        ('available', 'متاح'),
        ('avl_for_rent', 'متاح للإيجار'),
        ('rented', 'مستأجر'),
        ('sold', 'تم البيع'),
        ('reserved', 'محجوز'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان الكتاب")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="المؤلف")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="التصنيف")
    description = models.TextField(verbose_name="الوصف")
    pages = models.PositiveIntegerField(verbose_name="عدد الصفحات")
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="الرقم الدولي")
    
    # معلومات السعر
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="سعر الشراء")
    retal_price_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="سعر الإيجار اليومي")
    retal_period = models.PositiveIntegerField(blank=True, null=True, verbose_name="مدة الإيجار (أيام)")
    
    # حالة الكتاب
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="الحالة")
    
    # الوسائط
    book_image = models.ImageField(upload_to=book_image_path, blank=True, null=True, verbose_name="صورة الغلاف")
    book_file = models.FileField(upload_to=book_file_path, blank=True, null=True, verbose_name="ملف الكتاب")
    
    # التواريخ
    published_date = models.DateField(verbose_name="تاريخ النشر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "كتاب"
        verbose_name_plural = "الكتب"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.author.name}"
    
    @property
    def total_rental_price(self):
        """حساب إجمالي سعر الإيجار"""
        if self.retal_price_day and self.retal_period:
            return self.retal_price_day * self.retal_period
        return 0
    
    @property
    def is_available_for_rent(self):
        """التحقق من إمكانية استئجار الكتاب"""
        return self.status == 'avl_for_rent'
    
    @property
    def is_available_for_sale(self):
        """التحقق من إمكانية شراء الكتاب"""
        return self.status == 'available'
    
    def get_status_display_class(self):
        """الحصول على كلاس CSS للحالة"""
        status_classes = {
            'available': 'success',
            'avl_for_rent': 'warning',
            'rented': 'info',
            'sold': 'danger',
            'reserved': 'secondary'
        }
        return status_classes.get(self.status, 'secondary')

class Customer(models.Model):
    """نموذج العملاء"""
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    address = models.TextField(verbose_name="العنوان")
    national_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية الوطنية")
    
    # معلومات إضافية
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")
    occupation = models.CharField(max_length=100, blank=True, null=True, verbose_name="المهنة")
    
    # التواريخ
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def total_rentals(self):
        """عدد استعارات العميل"""
        return self.rental_set.count()
    
    @property
    def active_rentals(self):
        """الاستعارات النشطة"""
        return self.rental_set.filter(is_active=True).count()

class Rental(models.Model):
    """نموذج استعارات الكتب"""
    
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('returned', 'تم الإرجاع'),
        ('overdue', 'متأخر'),
        ('cancelled', 'ملغي'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="الكتاب")
    
    # معلومات الاستعارة
    rental_date = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الاستعارة")
    return_date = models.DateTimeField(blank=True, null=True, verbose_name="تاريخ الإرجاع")
    due_date = models.DateTimeField(verbose_name="تاريخ الاستحقاق")
    rental_period = models.PositiveIntegerField(verbose_name="مدة الاستعارة (أيام)")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الإجمالي")
    
    # حالة الاستعارة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="الحالة")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    
    # معلومات إضافية
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "استعارة"
        verbose_name_plural = "الاستعارات"
        ordering = ['-rental_date']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['book']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"استعارة {self.book.title} - {self.customer.name}"
    
    def save(self, *args, **kwargs):
        """حساب تاريخ الاستحقاق والسعر الإجمالي تلقائياً"""
        if not self.due_date and self.rental_period:
            self.due_date = self.rental_date + timedelta(days=self.rental_period)
        
        if not self.total_price and self.book.retal_price_day and self.rental_period:
            self.total_price = self.book.retal_price_day * self.rental_period
        
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """التحقق من تأخر الاستعارة"""
        if self.is_active and timezone.now() > self.due_date:
            return True
        return False
    
    @property
    def days_remaining(self):
        """عدد الأيام المتبقية"""
        if self.is_active:
            remaining = self.due_date - timezone.now()
            return max(0, remaining.days)
        return 0
    
    @property
    def days_overdue(self):
        """عدد أيام التأخير"""
        if self.is_overdue:
            overdue = timezone.now() - self.due_date
            return overdue.days
        return 0

class Sale(models.Model):
    """نموذج مبيعات الكتب"""
    
    PAYMENT_METHODS = [
        ('cash', 'نقدي'),
        ('card', 'بطاقة ائتمان'),
        ('transfer', 'تحويل بنكي'),
        ('check', 'شيك'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="الكتاب")
    
    # معلومات البيع
    sale_date = models.DateTimeField(default=timezone.now, verbose_name="تاريخ البيع")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر البيع")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash', verbose_name="طريقة الدفع")
    
    # معلومات إضافية
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="رقم الفاتورة")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "بيع"
        verbose_name_plural = "المبيعات"
        ordering = ['-sale_date']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['book']),
            models.Index(fields=['invoice_number']),
        ]
    
    def __str__(self):
        return f"بيع {self.book.title} - {self.customer.name}"

class Review(models.Model):
    """نموذج تقييمات الكتب"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="الكتاب")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    
    # معلومات التقييم
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="التعليق")
    
    # التواريخ
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التقييم")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
        unique_together = ['book', 'customer']  # منع التقييم المكرر
        ordering = ['-created_at']
    
    def __str__(self):
        return f"تقييم {self.book.title} - {self.rating} نجوم"

class Wishlist(models.Model):
    """نموذج قائمة الرغبات"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="الكتاب")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    
    class Meta:
        verbose_name = "قائمة رغبات"
        verbose_name_plural = "قوائم الرغبات"
        unique_together = ['customer', 'book']  # منع التكرار
        ordering = ['-added_date']
    
    def __str__(self):
        return f"{self.book.title} في قائمة {self.customer.name}"

class Notification(models.Model):
    """نموذج الإشعارات"""
    
    TYPES = [
        ('rental_due', 'موعد استعارة'),
        ('rental_overdue', 'تأخر في الإرجاع'),
        ('new_book', 'كتاب جديد'),
        ('promotion', 'عرض ترويجي'),
        ('system', 'إشعار نظام'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    title = models.CharField(max_length=200, verbose_name="عنوان الإشعار")
    message = models.TextField(verbose_name="نص الإشعار")
    notification_type = models.CharField(max_length=20, choices=TYPES, verbose_name="نوع الإشعار")
    is_read = models.BooleanField(default=False, verbose_name="تم القراءة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")
    
    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural = "الإشعارات"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.customer.name}"

# إشارات (Signals) - يمكن إضافتها في ملف signals.py منفصل
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Rental)
def update_book_status_on_rental(sender, instance, created, **kwargs):
    """تحديث حالة الكتاب عند الاستعارة"""
    if created and instance.book.status == 'avl_for_rent':
        instance.book.status = 'rented'
        instance.book.save()

@receiver(post_save, sender=Sale)
def update_book_status_on_sale(sender, instance, created, **kwargs):
    """تحديث حالة الكتاب عند البيع"""
    if created:
        instance.book.status = 'sold'
        instance.book.save()