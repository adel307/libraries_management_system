from django.db import models
from django.contrib.auth.models import User
from my_books.models import Book

class CustomerBook(models.Model):
    """نموذج وسيط للكتب المملوكة"""
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'book'], name='unique_customer_purchased_book')  # ✅ تغيير الاسم
        ]
        verbose_name = "كتاب مملوك"
        verbose_name_plural = "الكتب المملوكة"

    def __str__(self):
        return f"{self.customer.name} - {self.book.title}"

class CustomerRentedBook(models.Model):
    """نموذج وسيط للكتب المستأجرة"""
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_start_date = models.DateTimeField(auto_now_add=True)  # ✅ تغيير الاسم
    rental_end_date = models.DateTimeField(null=True, blank=True)  # ✅ إضافة تاريخ انتهاء الإيجار
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ تغيير الاسم

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'book'], name='unique_customer_rented_book')  # ✅ تغيير الاسم
        ]
        verbose_name = "كتاب مستأجر"
        verbose_name_plural = "الكتب المستأجرة"

    def __str__(self):
        return f"{self.customer.name} - {self.book.title} (مستأجر)"

class Customer(models.Model):
    """نموذج العملاء"""
    user = models.ForeignKey(  # ✅ استخدام ForeignKey بدلاً من CharField
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="المستخدم"
    )
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    image = models.ImageField(upload_to='customers/%Y/%m/%d', blank=True, null=True, verbose_name="صورة الملف الشخصي")  # ✅ تحسين مسار الصور
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    address = models.TextField(verbose_name="العنوان")
    national_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية الوطنية")
    
    # الكتب المملوكة
    my_books = models.ManyToManyField(
        Book,
        through=CustomerBook,
        blank=True,
        verbose_name="كتبي المملوكة",
        related_name='owned_by_customers'  # ✅ تغيير related_name
    )

    # الكتب المستأجرة
    my_rented_books = models.ManyToManyField(
        Book,
        through=CustomerRentedBook,
        blank=True,
        verbose_name="كتبي المستأجرة",
        related_name='rented_by_customers'  # ✅ تغيير related_name
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
        return self.my_rented_books.count()
    
    @property
    def active_rentals(self):
        """الاستعارات النشطة"""
        return self.my_rented_books.filter(status='rented').count()

    @property
    def sold_books_count(self):
        """عدد الكتب المباعة"""
        return self.my_books.count()
    
    @property
    def rented_books_count(self):
        """عدد الكتب المستأجرة"""
        return self.my_rented_books.count()

    @property
    def total_spent(self):
        """إجمالي ما أنفقه العميل"""
        purchased_books = CustomerBook.objects.filter(customer=self)
        total = sum([book.purchase_price for book in purchased_books if book.purchase_price])
        return total