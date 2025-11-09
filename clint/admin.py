from django.contrib import admin
from .models import Customer, CustomerBook, CustomerRentedBook, Book

admin.site.site_header = 'موقع إدارة المكتبات'
admin.site.site_title = 'LMS'

class CustomerBookInline(admin.TabularInline):
    model = CustomerBook
    extra = 1
    can_delete = True
    fields = ['book', 'purchase_price', 'purchase_date']
    readonly_fields = ['purchase_date']
    
    # تصفية الكتب لعرض المباعة فقط في قائمة الاختيار
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='sold')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CustomerRentedBookInline(admin.TabularInline):
    model = CustomerRentedBook
    extra = 1
    can_delete = True
    fields = ['book', 'rental_price', 'rental_start_date']  # ✅ استخدام الحقول الصحيحة
    readonly_fields = ['rental_start_date']  # ✅ استخدام الحقول الصحيحة
    
    # تصفية الكتب لعرض المستأجرة فقط في قائمة الاختيار
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='rented')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'email', 'phone', 'national_id', 
        'date_of_birth', 'occupation', 'created_at', 'updated_at',
        'get_sold_books_count', 'get_rented_books_count'  # ✅ إضافة الدوال المحسنة
    ]
    list_editable = ['name', 'email', 'phone', 'national_id', 'date_of_birth', 'occupation']
    list_display_links = ['id']
    search_fields = ['name', 'email', 'phone', 'national_id', 'occupation']
    
    # ✅ إضافة كلا الـ Inlines معاً
    inlines = [CustomerBookInline, CustomerRentedBookInline]

    # ✅ تعريف الدوال بشكل صحيح
    def get_sold_books_count(self, obj):
        return obj.my_books.count()  # أو obj.my_books.filter(status='sold').count()
    get_sold_books_count.short_description = 'الكتب المملوكة'

    def get_rented_books_count(self, obj):
        return obj.my_rented_books.count()  # أو obj.my_rented_books.filter(status='rented').count()
    get_rented_books_count.short_description = 'الكتب المستأجرة'

admin.site.register(Customer, CustomerAdmin)

@admin.register(CustomerBook)
class CustomerBookAdmin(admin.ModelAdmin):
    list_display = ['customer', 'book', 'purchase_price', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['customer__name', 'book__title']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='sold')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(CustomerRentedBook)
class CustomerRentedBookAdmin(admin.ModelAdmin):
    list_display = ['customer', 'book', 'rental_price', 'rental_start_date']  # ✅ استخدام الحقول الصحيحة
    list_filter = ['rental_start_date']  # ✅ استخدام الحقول الصحيحة
    search_fields = ['customer__name', 'book__title']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='rented')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)