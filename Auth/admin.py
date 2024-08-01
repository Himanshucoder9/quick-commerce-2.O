from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from Auth.models import User, CustomAdmin, Customer, WareHouse, Driver
from Auth.send_sms import send_approve_warehouse_sms

admin.site.unregister(Group)


# Base User Admin
class BaseUserAdmin:
    fieldsets = (
        ('User Info', {
            'fields': ('role', 'name', 'email', 'phone', 'dob', 'gender', 'profile',),
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'is_active',),
        }),
        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined',)
    search_fields = ('name', 'email', 'phone', 'role', 'gender')
    list_filter = ('name', 'email', 'gender', 'phone', 'role', 'is_active')
    ordering = ('phone',)
    list_per_page = 15

    def _profile(self, obj):
        return format_html(
            '<img src="{}" style="max-width:50px; max-height:50px; border-radius:50%;"/>'.format(obj.profile.url)
        ) if obj.profile else "No Profile"

    _profile.short_description = 'Profile'


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, UserAdmin):
    model = User
    list_display = ('name', '_profile', 'phone', 'email', 'gender', 'role', 'is_active',)

    add_fieldsets = (
        (None, {
            'fields': ('role', 'name', 'email', 'phone', 'gender', 'dob', 'profile', 'password1', 'password2',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # New user
            if obj.role == User.SUPERUSER:
                obj.is_staff = obj.is_active = obj.is_superuser = True
        else:  # Update user
            obj.is_superuser = obj.role == User.SUPERUSER
        obj.save()


@admin.register(CustomAdmin)
class CustomAdminAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ('name', 'email', 'phone', 'gender', '_profile', 'is_active')

    add_fieldsets = (
        (None, {
            'fields': ('role', 'name', 'email', 'phone', 'gender', 'dob', 'profile', 'password1', 'password2',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.role = User.SUPERUSER
        super().save_model(request, obj, form, change)


@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ('name', 'email', 'phone', 'gender', '_profile', 'is_active', 'approved')

    add_fieldsets = (
        (None, {
            'fields': ('role', 'name', 'email', 'phone', 'gender', 'dob', 'profile', 'password1', 'password2',)
        }),
    )


@admin.register(WareHouse)
class WareHouseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Personal Info', {
            'fields': ('role', 'name', 'email', 'phone', 'dob', 'gender', 'profile'),
        }),
        ('WareHouse Info', {
            'fields': ('warehouse_id', 'warehouse_name', 'license', 'gst_no', 'fssai_no', 'operation_area',
                       'warehouse_image', 'warehouse_image_owner',),
        }),
        ('Identity Details', {
            'fields': ('identity', 'document',),
        }),
        ('Address', {
            'fields': ('building_name', 'street_name', 'zip', 'city', 'state', 'full_address', 'latitude', 'longitude'),
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'approved'),
        }),
        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),
    )

    def _warehouse_image_owner(self, obj):
        return format_html(
            '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.warehouse_image_owner.url)
        ) if obj.warehouse_image_owner else "No Image"

    actions = ['approve_warehouses', 'disapprove_warehouses']

    def approve_warehouses(self, request, queryset):
        queryset.update(approved=True)
        for warehouse in queryset:
            send_approve_warehouse_sms(warehouse.user)
        self.message_user(request, "Selected warehouses have been approved and notified by SMS.")

    def disapprove_warehouses(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected warehouses have been disapproved.")

    approve_warehouses.short_description = 'Approve selected warehouses'
    disapprove_warehouses.short_description = 'Disapprove selected warehouses'

    list_display = ('name', 'email', 'phone', 'warehouse_id', 'warehouse_name', 'operation_area',
                    '_warehouse_image_owner', 'approved')

    search_fields = ('name', 'warehouse_name', 'identity', 'fssai_no', 'warehouse_id', 'operation_area')
    list_filter = ('approved',)

    add_fieldsets = (
        ('Personal Info', {
            'fields': ('role', 'name', 'email', 'phone', 'dob', 'gender', 'profile', 'password1', 'password2',)
        }),
        ('WareHouse Info', {
            'fields': ('warehouse_id', 'warehouse_name', 'license', 'gst_no', 'fssai_no', 'operation_area',
                       'warehouse_image', 'warehouse_image_owner',),
        }),
        ('Identity Details', {
            'fields': ('identity', 'document',),
        }),
        ('Address', {
            'fields': ('building_name', 'street_name', 'zip', 'city', 'state', 'full_address', 'latitude', 'longitude'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'approved'),
        }),
    )
    ordering = ('phone',)
    list_per_page = 15


@admin.register(Driver)
class DriverAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Personal Info', {
            'fields': ('role', 'warehouse', 'name', 'email', 'phone', 'dob', 'gender', 'profile',),
        }),
        ('Driver Info', {
            'fields': ('license', 'license_front', 'license_back', 'vehicle_no', 'is_free'),
        }),
        ('Identity Details', {
            'fields': ('aadhar_no', 'pan_no', 'aadhar_document', 'pan_document', 'address'),
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'approved'),
        }),
        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),
    )

    actions = ['approve_drivers', 'disapprove_drivers']

    def approve_drivers(self, request, queryset):
        queryset.update(approved=True)
        for driver in queryset:
            send_approve_warehouse_sms(driver.user)
        self.message_user(request, "Selected drivers have been approved and notified by SMS.")

    def disapprove_drivers(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected drivers have been disapproved.")

    approve_drivers.short_description = 'Approve selected drivers'
    disapprove_drivers.short_description = 'Disapprove selected drivers'

    list_display = ('name', 'email', 'phone', 'gender', '_profile', 'is_active', 'is_free')
    list_filter = ('name', 'email', 'gender', 'phone', 'role', 'is_active')
    search_fields = ('name', 'email', 'phone', 'role', 'gender')

    add_fieldsets = (
        ('Personal Info', {
            'fields': (
            'role', 'warehouse', 'name', 'email', 'phone', 'dob', 'gender', 'profile', 'password1', 'password2',)
        }),
        ('Driver Info', {
            'fields': ('license', 'license_front', 'license_back', 'vehicle_no', 'is_free'),
        }),
        ('Identity Details', {
            'fields': ('aadhar_no', 'pan_no', 'aadhar_document', 'pan_document', 'address'),
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'approved'),
        }),
    )
    ordering = ('phone',)
    list_per_page = 15
