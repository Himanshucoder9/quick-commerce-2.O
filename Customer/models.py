from django.db import models
from Master.models import TimeStamp
from Auth.models import User
from Master.myvalidator import mobile_validator

class ShippingAddress(TimeStamp):
    ADDRESS_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('hotel', 'Hotel'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200, verbose_name="customer name")
    phone = models.CharField(
        verbose_name="customer mobile number",
        max_length=13,
        validators=[mobile_validator],
        help_text="Alphabets and special characters are not allowed.",
    )
    address_type = models.CharField(max_length=10, choices=ADDRESS_CHOICES, default='home')
    building_name = models.CharField(max_length=255, verbose_name="Flat/House No./Building Name")
    floor = models.CharField(max_length=20, verbose_name="Floor", blank=True, null=True)
    landmark = models.CharField(max_length=255, verbose_name="Nearby Landmark", blank=True, null=True)
    latitude = models.DecimalField(verbose_name="Latitude", max_digits=9, decimal_places=6)
    longitude = models.DecimalField(verbose_name="Longitude", max_digits=9, decimal_places=6)
    full_address = models.TextField(verbose_name="full address")

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f"{self.customer_name} | {self.address_type}"

###################################################  Favorite #############################################
class Favorite(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.product.title}"

