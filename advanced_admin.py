from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from .models import (
    Category, Author, Book, Customer, 
    Rental, Sale, Review, Wishlist, Notification
)


# إعدادات الموقع الإداري
admin.site.site_header = "نظام إدارة المكتبات"
admin.site.site_title = "لوحة التحكم - المكتبة"
admin.site.index_title = "مرحباً بك في نظام إدارة المكتبات"


class BaseAdmin(admin.ModelAdmin):
    """فئة أساسية للإعدادات المشتركة"""
    list_per_page = 25
    save_on_top = True
    date_hierarchy = 'created_at'


# فلاتر مخصصة
class StatusFilter(admin.SimpleListFilter):
    """فلتر مخصص لحالة الكتاب"""
    title = 'حالة الكتاب'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('available', 'متاح للشراء'),
            ('avl_for_rent', 'متاح للإيجار'),
            ('rented', 'مستأجر'),
            ('sold', 'تم البيع'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class RentalStatusFilter(admin.SimpleListFilter):
    """فلتر مخصص لحالة الاستعارة"""
    title = 'حالة الاستعارة'
    parameter_name = 'rental_status'

    def lookups(self, request, model_admin):
        return [
            ('active', 'نشط'),
            ('overdue', 'متأخر'),
            ('returned', 'تم الإرجاع'),
        ]

    def queryset(self, request, queryset):
        from django.utils import timezone
        if self.value() == 'active':
            return queryset.filter(is_active=True, due_date__gte=timezone.now())
        elif self.value() == 'overdue':
            return queryset.filter(is_active=True, due_date__lt=timezone.now())
        elif self.value() == 'returned':
            return queryset.filter(is_active=False)
        return queryset


# إجراءات مخصصة
def make_available(modeladmin, request, queryset):
    """جعل الكتب المحددة متاحة"""
    queryset.update(status='available')
make_available.short_description = "جعل الكتب المحددة متاحة للشراء"

def make_available_for_rent(modeladmin, request, queryset):
    """جعل الكتب المحددة متاحة للإيجار"""
    queryset.update(status='avl_for_rent')
make_available_for_rent.short_description = "جعل الكتب المحددة متاحة للإيجار"

def mark_as_returned(modeladmin, request, queryset):
    """تحديد الاستعارات كمُرجعة"""
    from django.utils import timezone
    queryset.update(
        is_active=False,
        status='returned',
        return_date=timezone.now()
    )
mark_as_returned.short_description = "تحديد الاستعارات كمُرجعة"

def send_promotion_notification(modeladmin, request, queryset):
    """إرسال إشعار ترويجي للعملاء المحددين"""
    from django.utils import timezone
    for customer in queryset:
        Notification.objects.create(
            customer=customer,
            title="عرض ترويجي جديد",
            message="لدينا عروض وتخفيضات جديدة على مجموعة من الكتب. تفضل بزيارة مكتبتنا!",
            notification_type='promotion'
        )
    modeladmin.message_user(request, f"تم إرسال الإشعارات إلى {queryset.count()} عميل")
send_promotion_notification.short_description = "إرسال إشعار ترويجي"


# نماذج Admin المخصصة
@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """إدارة التصنيفات"""
    list_display = ['name', 'book_count', 'created_at']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            book_count=Count('book')
        )
    
    def book_count(self, obj):
        return obj.book_count
    book_count.short_description = 'عدد الكتب'
    book_count.admin_order_field = 'book_count'


@admin.register(Author)
class AuthorAdmin(BaseAdmin):
    """إدارة المؤلفين"""
    list_display = ['name', 'nationality', 'book_count', 'birth_date']
    list_display_links = ['name']
    search_fields = ['name', 'bio']
    list_filter = ['nationality', 'birth_date']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            book_count=Count('book')
        )
    
    def book_count(self, obj):
        return obj.book_count
    book_count.short_description = 'عدد الكتب'
    book_count.admin_order_field = 'book_count'


@admin.register(Book)
class BookAdmin(BaseAdmin):
    """إدارة الكتب"""
    list_display = [
        'title', 'author', 'category', 'status_badge', 
        'price', 'retal_price_day', 'created_at', 'book_image_preview'
    ]
    list_display_links = ['title']
    list_filter = [StatusFilter, 'category', 'author', 'created_at']
    search_fields = ['title', 'author__name', 'description', 'isbn']
    readonly_fields = ['created_at', 'updated_at', 'book_image_preview_large']
    actions = [make_available, make_available_for_rent]
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'author', 'category', 'description', 'pages', 'isbn')
        }),
        ('المعلومات المالية', {
            'fields': ('price', 'retal_price_day', 'retal_period', 'total_rental_price')
        }),
        ('الحالة والوسائط', {
            'fields': ('status', 'book_image', 'book_image_preview_large', 'book_file')
        }),
        ('التواريخ', {
            'fields': ('published_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """عرض حالة الكتاب كبادجة ملونة"""
        status_classes = {
            'available': 'success',
            'avl_for_rent': 'warning',
            'rented': 'info',
            'sold': 'danger',
            'reserved': 'secondary'
        }
        color = status_classes.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'
    
    def book_image_preview(self, obj):
        """معاينة مصغرة لصورة الكتاب في القائمة"""
        if obj.book_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.book_image.url
            )
        return "-"
    book_image_preview.short_description = 'الصورة'
    
    def book_image_preview_large(self, obj):
        """معاينة كبيرة لصورة الكتاب في صفحة التعديل"""
        if obj.book_image:
            return format_html(
                '<img src="{}" width="200" style="object-fit: cover; border-radius: 10px; border: 2px solid #ddd;" />',
                obj.book_image.url
            )
        return "لا توجد صورة"
    book_image_preview_large.short_description = 'معاينة الصورة'
    book_image_preview_large.allow_tags = True
    
    def total_rental_price(self, obj):
        """عرض السعر الإجمالي للإيجار"""
        return f"${obj.total_rental_price}" if obj.total_rental_price else "-"
    total_rental_price.short_description = 'السعر الإجمالي للإيجار'


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    """إدارة العملاء"""
    list_display = [
        'name', 'email', 'phone', 'national_id', 
        'total_rentals', 'active_rentals', 'created_at'
    ]
    list_display_links = ['name']
    search_fields = ['app_name','name', 'email', 'phone', 'national_id', 'address']
    list_filter = ['created_at', 'occupation']
    readonly_fields = ['created_at', 'updated_at']
    actions = [send_promotion_notification]
    
    fieldsets = (
        ('المعلومات الشخصية', {
            'fields': ('name', 'email', 'phone', 'national_id', 'date_of_birth', 'occupation')
        }),
        ('العنوان', {
            'fields': ('address',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            rental_count=Count('rental')
        )
    
    def total_rentals(self, obj):
        return obj.rental_count
    total_rentals.short_description = 'إجمالي الاستعارات'
    total_rentals.admin_order_field = 'rental_count'


@admin.register(Rental)
class RentalAdmin(BaseAdmin):
    """إدارة الاستعارات"""
    list_display = [
        'customer', 'book', 'rental_date', 'due_date', 
        'return_date', 'status_badge', 'is_active', 'days_remaining_display'
    ]
    list_display_links = ['customer', 'book']
    list_filter = [RentalStatusFilter, 'rental_date', 'due_date', 'status']
    search_fields = ['customer__name', 'book__title', 'notes']
    readonly_fields = ['created_at', 'days_remaining_display', 'days_overdue_display']
    actions = [mark_as_returned]
    
    fieldsets = (
        ('معلومات الاستعارة', {
            'fields': ('customer', 'book', 'rental_period', 'total_price')
        }),
        ('التواريخ', {
            'fields': ('rental_date', 'due_date', 'return_date')
        }),
        ('الحالة والمعلومات', {
            'fields': ('status', 'is_active', 'notes', 'days_remaining_display', 'days_overdue_display')
        }),
    )
    
    def status_badge(self, obj):
        """عرض حالة الاستعارة كبادجة ملونة"""
        status_classes = {
            'active': 'success',
            'returned': 'secondary',
            'overdue': 'danger',
            'cancelled': 'warning'
        }
        color = status_classes.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'
    
    def days_remaining_display(self, obj):
        """عرض الأيام المتبقية"""
        if obj.is_active:
            days = obj.days_remaining
            color = 'success' if days > 3 else 'warning' if days > 0 else 'danger'
            return format_html(
                '<span class="badge badge-{}">{} أيام</span>',
                color, days
            )
        return "-"
    days_remaining_display.short_description = 'الأيام المتبقية'
    
    def days_overdue_display(self, obj):
        """عرض أيام التأخير"""
        if obj.is_overdue:
            return format_html(
                '<span class="badge badge-danger">{} أيام</span>',
                obj.days_overdue
            )
        return "-"
    days_overdue_display.short_description = 'أيام التأخير'


@admin.register(Sale)
class SaleAdmin(BaseAdmin):
    """إدارة المبيعات"""
    list_display = [
        'customer', 'book', 'sale_date', 'sale_price', 
        'payment_method_display', 'invoice_number'
    ]
    list_display_links = ['customer', 'book']
    list_filter = ['sale_date', 'payment_method']
    search_fields = ['customer__name', 'book__title', 'invoice_number']
    readonly_fields = ['created_at']
    
    def payment_method_display(self, obj):
        """عرض طريقة الدفع كبادجة"""
        method_classes = {
            'cash': 'success',
            'card': 'primary',
            'transfer': 'info',
            'check': 'warning'
        }
        color = method_classes.get(obj.payment_method, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_payment_method_display()
        )
    payment_method_display.short_description = 'طريقة الدفع'


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    """إدارة التقييمات"""
    list_display = ['book', 'customer', 'rating_stars', 'created_at']
    list_display_links = ['book', 'customer']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'customer__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def rating_stars(self, obj):
        """عرض التقييم كنجوم"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = {
            1: 'danger',
            2: 'warning',
            3: 'info',
            4: 'primary',
            5: 'success'
        }.get(obj.rating, 'secondary')
        
        return format_html(
            '<span style="color: gold; font-size: 16px;">{}</span> <span class="badge badge-{}">{}</span>',
            stars, color, obj.rating
        )
    rating_stars.short_description = 'التقييم'


@admin.register(Wishlist)
class WishlistAdmin(BaseAdmin):
    """إدارة قوائم الرغبات"""
    list_display = ['customer', 'book', 'added_date']
    list_display_links = ['customer', 'book']
    list_filter = ['added_date']
    search_fields = ['customer__name', 'book__title']


@admin.register(Notification)
class NotificationAdmin(BaseAdmin):
    """إدارة الإشعارات"""
    list_display = ['customer', 'title', 'notification_type_badge', 'is_read', 'created_at']
    list_display_links = ['customer', 'title']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['customer__name', 'title', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    def notification_type_badge(self, obj):
        """عرض نوع الإشعار كبادجة"""
        type_classes = {
            'rental_due': 'warning',
            'rental_overdue': 'danger',
            'new_book': 'success',
            'promotion': 'info',
            'system': 'secondary'
        }
        color = type_classes.get(obj.notification_type, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_notification_type_display()
        )
    notification_type_badge.short_description = 'نوع الإشعار'


# لوحة تحكم مخصصة
class LibraryAdminDashboard(admin.AdminSite):
    """لوحة تحكم مخصصة للمكتبة"""
    site_header = "نظام إدارة المكتبات المتكامل"
    site_title = "إدارة المكتبة"
    index_title = "لوحة التحكم الرئيسية"

    def index(self, request, extra_context=None):
        """إضافة إحصائيات إلى الصفحة الرئيسية"""
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # إحصائيات أساسية
        stats = {
            'total_books': Book.objects.count(),
            'total_customers': Customer.objects.count(),
            'active_rentals': Rental.objects.filter(is_active=True).count(),
            'total_sales': Sale.objects.count(),
            'overdue_rentals': Rental.objects.filter(
                is_active=True, 
                due_date__lt=timezone.now()
            ).count(),
        }
        
        # إحصائيات المبيعات
        recent_sales = Sale.objects.filter(
            sale_date__gte=timezone.now() - timedelta(days=30)
        )
        stats['recent_sales_total'] = recent_sales.aggregate(
            total=Sum('sale_price')
        )['total'] or 0
        
        # كتب الأكثر استعارة
        popular_books = Book.objects.annotate(
            rental_count=Count('rental')
        ).order_by('-rental_count')[:5]
        
        extra_context = extra_context or {}
        extra_context.update({
            'stats': stats,
            'popular_books': popular_books,
        })
        
        return super().index(request, extra_context)


# إلغاء تسجيل Group الافتراضي
admin.site.unregister(Group)

# إضافة CSS مخصصة
class Media:
    css = {
        'all': ('admin/css/custom_admin.css',)
    }