from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from imagekit.models import ProcessedImageField
from Auth.managers import UserManager
from Master.models import Address
from Master.myvalidator import (numeric, mobile_validator, minimum, maximum, pan_validator, gst_validator, )


class User(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    ROLE_CHOICES = [
        ('SU', 'Superuser'),
        ('WH', 'Warehouse'),
        ('CU', 'Customer'),
        ('DR', 'Driver'),
    ]

    username = None
    first_name = None
    last_name = None
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, verbose_name=_("role"))
    name = models.CharField(max_length=200, verbose_name=_("full name"))
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name=_("email address"))
    phone = models.CharField(
        max_length=13,
        validators=[mobile_validator],
        unique=True,
        verbose_name=_("mobile number"),
        help_text=_("Alphabets and special characters are not allowed (eg.+911234567890)."),
    )
    dob = models.DateField(blank=True, null=True, verbose_name=_("date of birth"))
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True, verbose_name=_("gender"))
    profile = ProcessedImageField(
        upload_to='auth/user/profile/',
        format='WEBP',
        options={'quality': 50},
        blank=True, null=True,
        verbose_name=_("profile photo"),
    )
    is_staff = models.BooleanField(default=False, verbose_name=_("staff status"),
                                   help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(default=False, verbose_name=_("active"),
                                    help_text=_("Unselect this instead of deleting accounts."))

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name", "role"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class CustomAdmin(User):
    class Meta:
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")


class WareHouse(User, Address):
    IDENTITY_CHOICES = (
        ('Aadhar Card', 'Aadhar Card'),
        ('Pan Card', 'Pan Card'),
        ('Driving Licence', 'Driving Licence'),
        ('Voter ID', 'Voter ID'),
    )

    warehouse_no = models.CharField(unique=True, max_length=15, verbose_name="warehouse number")
    warehouse_name = models.CharField(max_length=100, verbose_name=_("registered warehouse name"))
    license = models.FileField(
        upload_to='auth/warehouse/license',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        verbose_name=_("license proof"),
        help_text=_("Upload license proof.")
    )
    identity = models.CharField(max_length=50, choices=IDENTITY_CHOICES, verbose_name=_("identity proof"))
    document = models.FileField(
        upload_to='auth/warehouse/identity',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        verbose_name=_("identity document"),
        help_text=_("Upload Identity Document.")
    )
    gst_no = models.CharField(max_length=15, verbose_name=_("GSTIN number"), validators=[gst_validator], blank=True,
                              null=True)
    fssai_no = models.CharField(max_length=15, verbose_name=_("FSSAI number"), blank=True, null=True)
    operation_area = models.CharField(max_length=200, verbose_name=_("area of operation"))
    warehouse_image = ProcessedImageField(
        upload_to='auth/warehouse/shop/',
        format='WEBP',
        options={'quality': 50},
        blank=True, null=True,
        verbose_name=_("shop image"),
        help_text=_("Upload warehouse image.")
    )
    warehouse_image_owner = ProcessedImageField(
        upload_to='auth/warehouse/shop_with_owner/',
        format='WEBP',
        options={'quality': 50},
        blank=True, null=True,
        verbose_name=_("shop image with owner"),
        help_text=_("Upload warehouse image with owner.")
    )
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))

    def save(self, *args, **kwargs):
        if not self.warehouse_no:
            last_object = WareHouse.objects.order_by('-id').first()
            if last_object and last_object.warehouse_no:
                last_warehouse_no = last_object.warehouse_no
                warehouse_no_prefix = last_warehouse_no[:-3]
                warehouse_no_suffix = last_warehouse_no[-3:]
                new_suffix = str(int(warehouse_no_suffix) + 1).zfill(3)
                self.warehouse_no = f"{warehouse_no_prefix}{new_suffix}"
            else:
                self.warehouse_no = "WH0001"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Warehouse - {self.warehouse_name}"

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")


class Customer(User):
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class Driver(User):
    warehouse_assigned = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name='drivers',
                                  verbose_name=_("warehouse"))
    address = models.TextField(verbose_name=_("Address"))
    license = models.CharField(max_length=16, verbose_name=_("DL number"))
    license_front = models.ImageField(upload_to='driver/license', verbose_name=_("license front image"))
    license_back = models.ImageField(upload_to='driver/license', verbose_name=_("license back image"))
    aadhar_no = models.CharField(
        max_length=12,
        validators=[numeric(_("Aadhar Number")), minimum(12, _("Aadhar number")), maximum(12, 'Aadhar number')],
        verbose_name=_("Aadhar Number"),
        help_text=_("Only numbers are allowed.")
    )
    pan_no = models.CharField(max_length=10, validators=[pan_validator], blank=True, null=True,
                              verbose_name=_("Pan Number"))
    aadhar_document = models.FileField(
        upload_to='driver/aadhar',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        verbose_name=_("Aadhar Document"),
        help_text=_("Upload Aadhar card.")
    )
    pan_document = models.FileField(
        upload_to='driver/pan',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        verbose_name=_("Pan Document"),
        help_text=_("Upload Pan card.")
    )
    vehicle_no = models.CharField(max_length=10, verbose_name=_("vehicle number"))
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))
    is_free = models.BooleanField(default=True, verbose_name=_("Is Free"))

    def __str__(self):
        return f"Driver - {self.name}"

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    otp = models.CharField(max_length=6, verbose_name=_("OTP"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTPs")


class ForgetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    otp = models.CharField(max_length=6, verbose_name=_("OTP"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("Forget OTP")
        verbose_name_plural = _("Forget OTPs")
