from django.apps import AppConfig


class ClintConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clint'

    def ready(self):
        import clint.signals  # تسجيل الإشارات