from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from Auth.models import WareHouse
# from Product.models import Product
from rest_framework.authtoken.models import TokenProxy as DRFToken
from import_export.admin import ImportExportModelAdmin
from .send_sms import send_approve_vendor_sms

admin.site.unregister(Group)
admin.site.unregister(DRFToken)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    resource_class = User
    fieldsets = (
        ('User Info', {
            'fields': (
                'role', 'name', 'email', 'phone', 'dob', 'gender', 'profile', 'password'),
        }),

        ('Status', {
            'fields': (
                'is_superuser', 'is_staff', 'is_active', 'is_verified',),
        }),

        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),

    )

    def _profile(self, obj):
        if obj.profile:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px; border-radius:50%;"/>'.format(obj.profile.url))
        else:
            return "No Profile"

    _profile.short_description = 'Profile'

    list_display = (
        'id', 'name', 'phone', 'email', 'gender', '_profile', 'role', 'is_verified', 'date_joined',)
    list_filter = ('name', 'email', 'gender', 'phone', 'is_verified', 'role',)
    readonly_fields = ('last_login', 'date_joined',)
    search_fields = ('name', 'email', 'phone', 'role',)
    add_fieldsets = (
        (None, {
            'fields': (
                'name', 'email', 'phone', 'dob', 'gender', 'profile', 'role', 'password1', 'password2',)}
         ),
    )
    ordering = ('email',)
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:  # This is a new user
            if obj.role == User.SUPERUSER:
                obj.is_staff = True
                obj.is_active = True
                obj.is_verified = True
                obj.is_superuser = True

        else:  # This is an existing user
            if obj.role == User.SUPERUSER:
                obj.is_staff = True
                obj.is_active = True
                obj.is_verified = True
                obj.is_superuser = True
            else:
                # obj.is_staff = False
                obj.is_superuser = False
        obj.save()


@admin.register(CustomAdmin)
class CustomAdminAdmin(ImportExportModelAdmin, UserAdmin):

    def _profile(self, obj):
        if obj.profile:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px; border-radius:50%;"/>'.format(obj.profile.url))
        else:
            return "No Profile"

    _profile.short_description = 'Profile'

    list_display = ('name', 'email', 'phone', 'gender', '_profile', 'is_active', 'date_joined')
    list_filter = ('is_active',)
    list_per_page = 10

    fieldsets = (
        ('Personal info', {'fields': ('name', 'email', 'phone', 'dob', 'gender', 'profile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'password1', 'password2'),
        }),
    )

    search_fields = ('phone', 'name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('phone',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        obj.role = User.SUPERUSER
        if not change:  # This is a new user
            if obj.role == User.SUPERUSER:
                obj.is_staff = True
                obj.is_active = True
                obj.is_verified = True
                obj.is_superuser = True

        else:  # This is an existing user
            if obj.role == User.SUPERUSER:
                obj.is_staff = True
                obj.is_active = True
                obj.is_verified = True
                obj.is_superuser = True

        obj.save()


@admin.register(WareHouse)
class VendorShopAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Shop Info', {
            'fields': (
                'user', 'vendor_id', 'shop_name', 'license', 'gst_no', 'fssai_no', 'business_category',
                'operation_area',
                'shop_image', 'shop_image_owner', "approved",),
        }),

        ('Identity Details', {
            'fields': (
                'identity', 'document',),
        }),

        ('Address', {
            'fields': (
                'building_name', 'street_name', 'zip', 'city', 'state', 'latitude', 'longitude', 'full_address'),
        }),

    )

    def _shop_image_with_owner(self, obj):
        if obj.shop_image_owner:
            return format_html(
                '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.shop_image_owner.url))
        else:
            return "No Image"

    actions = ['approve_vendors', 'disapprove_vendors']

    def approve_vendors(self, request, queryset):
        queryset.update(approved=True)
        for vendor in queryset:
            send_approve_vendor_sms(vendor.user)
        self.message_user(request, "Selected vendors have been approved and notified by SMS.")

    def disapprove_vendors(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected vendors have been disapproved.")

    approve_vendors.short_description = 'Approve selected vendors'
    disapprove_vendors.short_description = 'Disapprove selected vendors'

    readonly_fields = ['vendor_id', "approved"]
    list_display = (
        'user', 'vendor_id', 'shop_name', 'business_category', 'operation_area', '_shop_image_with_owner', "approved")
    search_fields = ('user__name', 'shop_name', 'identity', 'fssai_no', 'vendor_id', 'operation_area')
    list_filter = ('business_category', 'approved',)
    list_per_page = 10


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Customer Info', {
            'fields': ('user',),
        }),
    )

    # Function to get user email
    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def user_phone(self, obj):
        return obj.user.phone

    user_phone.short_description = 'Phone'

    def user_name(self, obj):
        return obj.user.name

    user_name.short_description = 'Full Name'

    def _profile(self, obj):
        if obj.user.profile:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px; border-radius:50%;"/>'.format(
                    obj.user.profile.url))
        else:
            return "No Profile"

    _profile.short_description = 'Profile'

    list_display = ('user', 'user_name', 'user_phone', 'user_email', '_profile')
    list_filter = ('user__name', 'user__phone', 'user__email',)
    search_fields = ('user__name', 'user__phone', 'user__email',)
    list_per_page = 10


@admin.register(Driver)
class DriverAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Driver Info', {
            'fields': (
                'user', 'vendor', 'license', 'license_front', 'license_back', 'vehicle_no', "approved", 'is_free'),
        }),

        ('Identity Details', {
            'fields': (
                'aadhar_no', 'pan_no', 'aadhar_document',
                'pan_document'),
        }),

        ('Address', {
            'fields': (
                'address',),
        }),

    )

    actions = ['approve_drivers', 'disapprove_drivers']

    def approve_drivers(self, request, queryset):
        queryset.update(approved=True)
        for driver in queryset:
            send_approve_vendor_sms(driver.user)
        self.message_user(request, "Selected drivers have been approved and notified by SMS.")

    def disapprove_drivers(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected drivers have been disapproved.")

    approve_drivers.short_description = 'Approve selected drivers'
    disapprove_drivers.short_description = 'Disapprove selected drivers'

    def _license_front(self, obj):
        if obj.license_front:
            return format_html(
                '<img src="{}" style="max-width:150px; max-height:150px;"/>'.format(
                    obj.license_front.url))
        else:
            return "No Image"

    _license_front.short_description = 'License Front'

    def _license_back(self, obj):
        if obj.license_back:
            return format_html(
                '<img src="{}" style="max-width:150px; max-height:150px;"/>'.format(
                    obj.license_back.url))
        else:
            return "No Image"

    _license_back.short_description = 'License Back'

    list_display = (
        'user', 'vendor', 'license', '_license_front', '_license_back', 'vehicle_no', 'address', "approved", 'is_free')
    search_fields = ('user__name', 'license',)
    list_filter = ('approved',)
    readonly_fields = ('approved',)
    list_per_page = 10
