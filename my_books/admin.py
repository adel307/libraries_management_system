from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.site_header = 'web site management'
admin.site.site_title = 'LMS'

class admin_Category(admin.ModelAdmin):
    list_display = ['id','name']
    list_editable = ['name']
    list_display_links = ['id']
    search_fields = ['name']
    # list_filter = ['cotegory','active']

class admin_Book(admin.ModelAdmin):
    list_display = ['id','title','auther','price','status','pages','catigery','active','retal_proid','retal_price_day',]
    list_editable = ['title','auther','price','status','pages','catigery','active','retal_proid','retal_price_day',]
    list_display_links = ['id']
    search_fields = ['title','auther','price','status','pages','active','retal_proid','retal_price_day',]
    # list_filter = ['moment']

admin.site.register(Category , admin_Category)
admin.site.register(Book , admin_Book)
