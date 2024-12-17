from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Region, Template, TemplateSKU, TemplateVersion, Service

@receiver(post_save, sender=Region)
@receiver(post_save, sender=Template)
@receiver(post_save, sender=TemplateSKU)
@receiver(post_save, sender=TemplateVersion)
@receiver(post_save, sender=Service)
def model_save_handler(sender, instance, created, **kwargs):
    if created:
        print(f"A new {sender.__name__} instance was created: {instance}")
    else:
        print(f"A {sender.__name__} instance was updated: {instance}")