from django.db import models
from my_books.models import *

# Create your models here.

class CustomerBook(models.Model):
    """نموذج وسيط للتحكم في العلاقة"""
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'book'], name='unique_customer_book')
        ]

class Customer(models.Model):
    """نموذج العملاء"""
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    image = models.ImageField(upload_to='photos3 %Y %m %d',blank=True,null=True,verbose_name="صورة الملف الشخصي")
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    address = models.TextField(verbose_name="العنوان")
    national_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية الوطنية")
    my_books = models.ManyToManyField(
        Book,
        through=CustomerBook,
        blank=True,
        verbose_name="كتبي المباعة",
        related_name='customers',
        limit_choices_to={'status': 'sold'}  # إضافة هذا
    )

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

    @property
    def sold_books(self):
        """الكتب المباعة فقط"""
        return self.my_books.filter(status='sold')


