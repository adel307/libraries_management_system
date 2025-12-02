# clint/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """إنشاء ملف عميل تلقائياً عند إنشاء مستخدم جديد"""
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    """حفظ ملف العميل عند تحديث المستخدم"""
    try:
        instance.customer.save()
    except Customer.DoesNotExist:
        Customer.objects.create(user=instance)