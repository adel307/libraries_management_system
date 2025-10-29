from django.contrib import admin
from .models import * 

admin.site.site_header = 'wed site management'
admin.site.site_title = 'LMS'

# تعريف Inline لعلاقة CustomerBook
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

class admin_Customer(admin.ModelAdmin):
    list_display = ['id','name','email','phone','address','national_id','date_of_birth','occupation','created_at','updated_at','get_sold_books_count']
    list_editable = ['name','email','phone','address','national_id','date_of_birth','occupation']
    list_display_links = ['id']
    search_fields = ['name','email','phone','address','national_id','occupation']
    
    # إزالة filter_horizontal واستخدام Inline فقط
    inlines = [CustomerBookInline]
    
    # دالة لعرض عدد الكتب المباعة فقط في قائمة العرض الرئيسية
    def get_sold_books_count(self, obj):
        return obj.my_books.filter(status='sold').count()
    get_sold_books_count.short_description = 'الكتب المباعة'

admin.site.register(Customer, admin_Customer)

# تسجيل CustomerBook بشكل منفصل
@admin.register(CustomerBook)
class CustomerBookAdmin(admin.ModelAdmin):
    list_display = ['customer', 'book', 'purchase_price', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['customer__name', 'book__title']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.filter(status='sold')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)