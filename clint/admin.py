from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.site_header = 'wed site management'
admin.site.site_title = 'LMS'

class admin_Customer(admin.ModelAdmin):
    list_display = ['id','name','email','phone','address','national_id','date_of_birth','occupation','created_at','updated_at']
    list_editable = ['name','email','phone','address','national_id','date_of_birth','occupation']
    list_display_links = ['id']
    search_fields = ['name','email','phone','address','national_id','occupation']
    # list_filter = ['moment']

admin.site.register(Customer,admin_Customer)
