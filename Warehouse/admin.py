from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Tax, Unit, PackagingType, Category, SubCategory, Product, Slider
)
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('rate', 'created_at', 'updated_at')
    search_fields = ('rate',)
    ordering = ('rate',)
    list_filter = ('rate', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 15

    fieldsets = (
        (_('Tax Info'), {
            'fields': ('rate',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'created_at', 'updated_at')
    search_fields = ('name', 'abbreviation',)
    ordering = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 15

    fieldsets = (
        (_('Unit Info'), {
            'fields': ('name', 'abbreviation')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(PackagingType)
class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'created_at', 'updated_at')
    search_fields = ('type',)
    ordering = ('type',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 15

    fieldsets = (
        (_('Packaging Type Info'), {
            'fields': ('type',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', '_image', 'is_deleted', 'created_at')
    list_filter = ('title', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 15

    fieldsets = (
        (_('Category Info'), {
            'fields': ('title', 'image', 'is_deleted'),
        }),
        (_('Timestamp'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        else:
            return _("No Image")

    _image.short_description = _("Image")


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'category', '_image', 'created_at', 'is_deleted',)
    list_filter = ('title', 'category', 'is_deleted')
    search_fields = ('title', 'category__title')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 15

    fieldsets = (
        (_('Sub Category Info'), {
            'fields': ('category', 'title', 'image', 'is_deleted'),
        }),
        (_('Timestamp'), {
            'fields': ('created_at', 'updated_at', 'slug'),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        else:
            return _("No Image")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'sku_no', 'category', '_image', 'price', 'stock_quantity', 'is_available', 'is_active',
        'is_deleted'
    )
    list_filter = (
        'category', 'subcategory', 'country_origin', 'packaging_type', 'is_available', 'is_active', 'is_deleted'
    )
    search_fields = ('title', 'sku_no')
    ordering = ('title',)
    readonly_fields = ('sku_no', 'created_at', 'updated_at')
    actions = ('active_products', 'disable_products')
    list_per_page = 15

    fieldsets = (
        (_('Product Info'), {
            'fields': (
                'sku_no', 'warehouse', 'title', 'size_unit', 'size', 'category', 'subcategory',
                'country_origin', 'packaging_type', 'description', 'price', 'discount', 'cgst', 'sgst', 'exp_date',
                'stock_quantity', 'stock_unit', 'reorder_level', 'is_available', 'is_active', 'is_deleted'
            )
        }),
        (_('Images'), {
            'fields': ('image1', 'image2', 'image3', 'image4', 'image5'),
            'classes': ('collapse',),
        }),
        (_('Attributes'), {
            'fields': (
                'attribute_key1', 'attribute_value1',
                'attribute_key2', 'attribute_value2',
                'attribute_key3', 'attribute_value3',
                'attribute_key4', 'attribute_value4',
                'attribute_key5', 'attribute_value5',
                'attribute_key6', 'attribute_value6',
                'attribute_key7', 'attribute_value7',
                'attribute_key8', 'attribute_value8'
            ),
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical', 'slug'),
        }),
        (_('Timestamp'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def _image(self, obj):
        if obj.image1:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image1.url))
        else:
            return _("No Image")

    def active_products(self, request, queryset):
        queryset.update(is_active=True)
        for product in queryset:
            product.save()
        self.message_user(request, "Selected products have been change to active.")

    def disable_products(self, request, queryset):
        queryset.update(is_active=False)
        for product in queryset:
            product.save()
        self.message_user(request, "Selected products have been change to in-active.")

    active_products.short_description = "Active selected products"
    disable_products.short_description = "In-active selected products"


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('warehouse', '_image', 'created_at', 'updated_at')
    search_fields = ('warehouse',)
    ordering = ('warehouse',)
    list_filter = ('warehouse', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 15

    fieldsets = (
        (_('Tax Info'), {
            'fields': ('warehouse', 'image', 'text', 'url')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        else:
            return _("No Image")
