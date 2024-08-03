from django.db import models
from Master.models import TimeStamp
from Auth.models import User, Customer, WareHouse
from Master.myvalidator import mobile_validator
from django.utils.translation import gettext_lazy as _
from Warehouse.models import Product


class ShippingAddress(TimeStamp):
    ADDRESS_CHOICES = [
        ("Home", "Home"),
        ("Work", "Work"),
        ("Hotel", "Hotel"),
        ("Other", "Other"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("customer"))
    customer_name = models.CharField(max_length=200, verbose_name=_("customer name"))
    customer_phone = models.CharField(
        max_length=13,
        validators=[mobile_validator],
        verbose_name=_("customer mobile number"),
        help_text=_("Alphabets and special characters are not allowed."),
    )
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_CHOICES,
        default="home",
        verbose_name=_("address type"),
    )
    building_name = models.CharField(max_length=255, verbose_name=_("Flat/House No./Building Name"))
    floor = models.CharField(max_length=20, verbose_name=_("Floor"), blank=True, null=True)
    landmark = models.CharField(max_length=255, verbose_name=_("Nearby Landmark"), blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Latitude"))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Longitude"))
    full_address = models.TextField(verbose_name=_("full address"))

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")

    def __str__(self):
        return f"{self.customer_name} | {self.address_type}"


class Favorite(TimeStamp):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="favorites", verbose_name=_("customer"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites", verbose_name=_("product"))

    class Meta:
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")

    def __str__(self):
        return f"{self.product.title}"


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart", verbose_name=_("customer"))

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"Cart for {self.customer.name} | {self.customer.phone}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE, verbose_name=_("cart"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("product"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in cart for {self.cart.customer.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    ]

    PAYMENT_METHOD = [
        ("Online", "Online"),
        ("COD", "Cash on Delivery"),
    ]

    order_number = models.CharField(max_length=15, verbose_name=_("Order Number"), unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", verbose_name=_("customer"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("total amount"))
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("shipping address"))
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending", verbose_name=_("order status"))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, verbose_name=_("payment method"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created date"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by("-id").first()
            if last_order:
                last_order_number = int(last_order.order_number.split('_')[1])
                new_order_number = f"ORD_{str(last_order_number + 1).zfill(10)}"
                self.order_number = new_order_number
            else:
                self.order_number = "ORD_0000000001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("order"))
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name="order_items", verbose_name=_("warehouse"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("product"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("item price"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created date"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in order {self.order.order_number}"


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("Online", "Online"),
        ("COD", "Cash on Delivery"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", verbose_name=_("customer"))
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name=_("order"))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name=_("payment method"))
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Razorpay Order ID"))
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Razorpay Payment ID"))
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("Razorpay Signature"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("amount"))
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=50, verbose_name=_("payment status"))
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name=_("payment date"))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"Payment for Order #{self.order.order_number}"
