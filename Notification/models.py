from django.db import models
from Auth.models import Customer, WareHouse, Driver, User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    is_read = models.BooleanField(default=False, verbose_name=_("is read"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")

    def __str__(self):
        return f"{self.title} for {self.user.name}"


class CustomerNotification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("customer"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    is_read = models.BooleanField(default=False, verbose_name=_("is read"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Customer Notification")
        verbose_name_plural = _("Customer Notifications")

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
        verbose_name = _("WareHouse Notification")
        verbose_name_plural = _("WareHouse Notifications")

    def __str__(self):
        return f"{self.title} for {self.warehouse.name}"


class DriverNotification(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name=_("driver"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    is_read = models.BooleanField(default=False, verbose_name=_("is read"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Driver Notification")
        verbose_name_plural = _("Driver Notifications")

    def __str__(self):
        return f"{self.title} for {self.driver.name}"
