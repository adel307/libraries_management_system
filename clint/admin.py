from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, CustomerBook, CustomerRentedBook, Book

admin.site.site_header = 'موقع إدارة المكتبات'
admin.site.site_title = 'LMS'

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'بيانات العميل'

class UserAdmin(BaseUserAdmin):
    inlines = [CustomerInline]

# إلغاء تسجيل User الافتراضي وإعادة تسجيله مع الـ Inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

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

# ✅ تم تعديل هذا الجزء: أصبح كلاس عادي وليس مسجل (لأنه سيتم استخدامه كـ Inline)
class CustomerRentedBookInline(admin.TabularInline):
    model = CustomerRentedBook
    extra = 1
    can_delete = True
    # 💡 إضافة rental_status
    fields = ['book', 'rental_price', 'rental_start_date', 'rental_status'] 
    readonly_fields = ['rental_start_date']
    
    # تصفية الكتب لعرض المستأجرة فقط في قائمة الاختيار
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='rented')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'email', 'phone', 'national_id', 
        'date_of_birth', 'occupation', 'created_at', 'updated_at',
        'get_sold_books_count', 'get_rented_books_count'
    ]
    list_editable = ['name', 'email', 'phone', 'national_id', 'date_of_birth', 'occupation']
    list_display_links = ['id']
    search_fields = ['name', 'email', 'phone', 'national_id', 'occupation']
    
    # ✅ استخدام الـ Inline المُعدل
    inlines = [CustomerBookInline, CustomerRentedBookInline]

    def get_sold_books_count(self, obj):
        return obj.my_books.count()
    get_sold_books_count.short_description = 'الكتب المملوكة'

    def get_rented_books_count(self, obj):
        return obj.my_rented_books.count()
    get_rented_books_count.short_description = 'الكتب المستأجرة'

# تم إلغاء التسجيل المكرر (admin.site.register(Customer, CustomerAdmin))

@admin.register(CustomerBook)
class CustomerBookAdmin(admin.ModelAdmin):
    list_display = ['customer', 'book', 'purchase_price', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['customer__name', 'book__title']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='sold')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ✅ تعديل CustomerRentedBookAdmin
@admin.register(CustomerRentedBook)
class CustomerRentedBookAdmin(admin.ModelAdmin):
    # 💡 إضافة rental_status إلى list_display
    list_display = ['customer', 'book', 'rental_price', 'rental_start_date', 'rental_status']
    # 💡 إضافة rental_status إلى list_filter
    list_filter = ['rental_start_date', 'rental_status']
    search_fields = ['customer__name', 'book__title']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='rented')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)