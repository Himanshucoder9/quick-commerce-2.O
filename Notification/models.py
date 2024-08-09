from django.db import models

from Auth.models import Customer, WareHouse
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomerNotification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("customer"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    is_read = models.BooleanField(default=False, verbose_name=_("is read"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return f"{self.title} for {self.customer.name}"


class WareHouseNotification(models.Model):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name=_("warehouse"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    is_read = models.BooleanField(default=False, verbose_name=_("is read"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return f"{self.title} for {self.warehouse.name}"
