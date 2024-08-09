from django.db import models
from Auth.models import Driver
from Master.models import TimeStamp
from Customer.models import Order
from django.utils.translation import gettext_lazy as _


class DeliveryAddress(TimeStamp):
    STATUS_CHOICE = (
        ("PROCESSING", "Processing"),
        ("PICKED_UP", "Picked Up"),
        ("IN_TRANSIT", "In Transit"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="pending", verbose_name=_("status"))
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, verbose_name=_("driver"))
    delivery_radius = models.FloatField(default=500, verbose_name=_("delivery radius"))
    orders = models.ForeignKey(Order,on_delete=models.CASCADE, related_name="deliveries", verbose_name=_("order"))
    otp = models.CharField(max_length=6, blank=True, null=True, verbose_name=_("OTP"))
    otp_created_at = models.DateTimeField(blank=True, null=True, verbose_name=_("OTP created"))

    def __str__(self):
        return f"Delivery to {self.orders.order_number} - Status: {self.status}"

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
