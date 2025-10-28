from django.db import models

# Create your models here.

class Customer(models.Model):
    """نموذج العملاء"""
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    image = models.ImageField(upload_to,blank=True,null=True,verbose_name="صورة الملف الشخصي")
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
