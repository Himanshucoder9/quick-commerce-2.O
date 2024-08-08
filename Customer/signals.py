from django.db.models.signals import post_save
from django.dispatch import receiver
from Customer.models import OrderItem, Order, CartItem, Cart
from django.db.models import F


@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock_quantity = F('stock_quantity') - instance.quantity
        product.save()
        product.refresh_from_db()
        if product.stock_quantity == 0:
            product.is_available = False
            product.save()


@receiver(post_save, sender=Order)
def clear_cart_items(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer

        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return

        CartItem.objects.filter(cart=cart).delete()