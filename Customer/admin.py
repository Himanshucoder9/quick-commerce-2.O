from django.contrib import admin
from .models import *
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from django.urls import reverse

# Register your models here.


@admin.register(ShippingAddress)
class ShippingAddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': (
                'customer', 'customer_name', 'customer_phone', 'address_type', 'building_name', 'floor', 'landmark', 'latitude',
                'longitude', 'full_address'),
        }),

        ('TimeStamp', {
            'fields': (
                'created_at', 'updated_at',),
        }),

    )

    list_display = [ 'customer', 'customer_name', 'customer_phone', 'address_type', 'building_name', 'floor', 'landmark']
    list_filter = ('customer_name', 'address_type',)
    search_fields = ('customer_name',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(Favorite)
class FavoriteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': (
                'customer', 'product'),
        }),

        ('TimeStamp', {
            'fields': (
                'created_at', 'updated_at',),
        }),

    )

    list_display = ['customer', 'product']
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': ('customer',),
        }),
    )

    list_display = ['id', 'customer', ]
    list_filter = ('customer__name',)
    readonly_fields = ('customer',)
    search_fields = ('customer__name',)
    list_per_page = 15

    def has_add_permission(self, request):
        return False


@admin.register(CartItem)
class CartItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': (
                'cart', 'product', 'quantity',),
        }),

    )

    list_display = [ 'cart', 'product', 'quantity', ]
    readonly_fields = ('cart', 'product', 'quantity',)
    list_filter = ('product__title',)
    list_per_page = 10

    def has_add_permission(self, request):
        return False


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': ('customer', 'order_number', 'shipping_address', 'total_amount', 'payment_method', 'order_status', 'created_at'),
        }),
    )

    def _shipping_address(self, obj):
        if obj.shipping_address:
            link = reverse("admin:Product_shippingaddress_change", args=[obj.shipping_address.pk])
            address = f'<a href="{link}"> Address Type - {obj.shipping_address.address_type}, <br> Flat/House No./Building Name - {obj.shipping_address.building_name}, <br> Floor - {obj.shipping_address.floor} <br> Landmark -  {obj.shipping_address.landmark}</a>'
            return format_html(address)
        else:
            return "No Shipping Address"

    _shipping_address.short_description = "Shipping Address"

    def has_add_permission(self, request):
        return False

    list_display = ['order_number', 'customer', 'total_amount', 'order_status', 'payment_method', '_shipping_address', 'created_at']
    list_filter = ('customer__name', 'total_amount', 'shipping_address')
    search_fields = ('customer__name',)
    readonly_fields = ('created_at', 'order_number')
    list_per_page = 15


@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': (
                'order', 'warehouse', 'product', 'item_price', 'quantity', 'created_at'),
        }),
    )

    def has_add_permission(self, request):
        return False

    list_display = ['order', 'warehouse', 'product', 'quantity', 'item_price', 'created_at', ]
    list_filter = ('order', 'created_at')
    search_fields = ('order__product__title',)
    list_per_page = 15


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Payment Details', {
            'fields': (
                'customer', 'order', 'payment_method', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature',
                'payment_status', 'amount', 'razorpay_payment_status', 'payment_date'),
        }),
    )

    def has_add_permission(self, request):
        return False

    def _payment_status(self, obj):
        if obj.payment_status == 'Pending':
            return format_html('<span style="color: white;  background-color: orange; padding: 5px;">{}</span>',
                               'Pending')
        elif obj.payment_status == 'Completed':
            return format_html('<span style="color: white; background-color: green; padding: 5px;">{}</span>',
                               'Completed')
        elif obj.payment_status == 'Cancel':
            return format_html('<span style="color: white; background-color: red; padding: 5px;">{}</span>',
                               'Cancel')

    _payment_status.short_description = 'Payment Status'

    list_display = ['customer', 'order', 'razorpay_payment_id', 'amount', '_payment_status', 'payment_method',
                    'payment_date']
    list_filter = ('order', 'razorpay_payment_id', 'payment_status', 'payment_method', 'payment_date',)
    search_fields = ('order', 'razorpay_payment_id', 'payment_method',)
    readonly_fields = ('payment_date',)
    list_per_page = 15
