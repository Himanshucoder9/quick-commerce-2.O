from django.db.models.signals import post_save
from django.dispatch import receiver
from Customer.models import OrderItem, Order, CartItem, Cart
from django.db.models import F
from Warehouse.models import Product


# @receiver(post_save, sender=OrderItem)
# def update_product_stock(sender, instance, created, **kwargs):
#     if created:
#         product = instance.product
#         product.stock_quantity = F('stock_quantity') - instance.quantity
#         product.save()
#         product.refresh_from_db()
#         if product.stock_quantity == 0:
#             product.is_available = False
#             product.save()

@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        # Update the stock quantity using F expression
        product.stock_quantity = F('stock_quantity') - instance.quantity
        product.save()  # Save the update to the database
        product.refresh_from_db()  # Refresh the instance from the database

        # Check the updated stock quantity and set availability
        if product.stock_quantity <= 0:
            product.is_available = False
        else:
            product.is_available = True

        product.save()  # Save the updated availability status


@receiver(post_save, sender=Order)
def clear_cart_items(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer

        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return

        CartItem.objects.filter(cart=cart).delete()