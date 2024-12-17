from django.conf import settings
from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usop.apps.services'
    
    def ready(self):
        import usop.apps.services.signals
        return super().ready()
