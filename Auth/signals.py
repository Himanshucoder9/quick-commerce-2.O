from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.CUSTOMER:
            Customer.objects.create(user=instance)

        if instance.role == User.DRIVER:
            Driver.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_or_update_custom_admin(sender, instance, created, **kwargs):
    if instance.role == User.SUPERUSER:
        fields = ['name', 'email', 'phone', 'dob', 'gender', 'profile', 'is_staff', 'is_active', 'is_verified',
                  'is_superuser', 'role', 'password']
        admin_data = {field: getattr(instance, field) for field in fields}
        CustomAdmin.objects.update_or_create(id=instance.id, defaults=admin_data)


