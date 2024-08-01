from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from Master.myvalidator import numeric, mobile_validator, minimum, maximum, alphanumeric, pan_validator, gst_validator
from django.core.validators import FileExtensionValidator
from imagekit.models import ProcessedImageField
from .managers import UserManager
from Master.models import Address, TimeStamp

# Create your models here.

class User(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    SUPERUSER = 'SU'
    warehouse = 'VE'
    CUSTOMER = 'CU'
    DRIVER = 'DR'

    ROLE_CHOICES = [
        (SUPERUSER, 'Superuser'),
        (warehouse, 'warehouse'),
        (CUSTOMER, 'Customer'),
        (DRIVER, 'Driver'),
    ]

    username = None
    first_name = None
    last_name = None
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, verbose_name=_("role"))
    name = models.CharField(max_length=200, verbose_name=_("full name"))
    email = models.EmailField(verbose_name=_("email address"), max_length=255, blank=True, null=True)
    phone = models.CharField(
        verbose_name=_("mobile number"),
        max_length=13,
        validators=[mobile_validator],
        help_text=_("Alphabets and special characters are not allowed (eg.+911234567890)."),
        unique=True,
    )
    dob = models.DateField(verbose_name=_("date of birth"), blank=True, null=True)
    gender = models.CharField(verbose_name=_("gender"), choices=GENDER_CHOICES, max_length=6, blank=True, null=True)
    profile = ProcessedImageField(
        verbose_name=_("profile photo"),
        upload_to='auth/user/profile/',
        format='WEBP',
        options={'quality': 50},
        blank=True, null=True
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=False,
        help_text=_("Designates whether this user should be treated as active. "
                    "Unselect this instead of deleting accounts."),
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name", "role"]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("All User")
        verbose_name_plural = _("All Users")


class CustomAdmin(User):
    class Meta:
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")

    def __str__(self):
        return f"{self.name}"


class WareHouse(User, Address):
    IDENTITY_CHOICES = (
        ('Aadhar Card', 'Aadhar Card'),
        ('Pan Card', 'Pan Card'),
        ('Driving Licence', 'Driving Licence'),
        ('Voter ID', 'Voter ID'),
    )
    warehouse_id = models.CharField(unique=True, max_length=15, verbose_name="warehouse id")
    warehouse_name = models.CharField(verbose_name=_("registered warehouse name"), max_length=100)
    license = models.FileField(
        verbose_name=_("license proof"),
        upload_to='auth/warehouse/license',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        help_text=_("Upload license proof.."))
    identity = models.CharField(choices=IDENTITY_CHOICES, max_length=50, verbose_name=_("identity proof"))
    document = models.FileField(
        verbose_name=_("identity document"),
        upload_to='auth/warehouse/identity',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        help_text=_("Upload Identity Document..."))
    gst_no = models.CharField(max_length=15, verbose_name=_("GSTIN number"), validators=[gst_validator], blank=True,
                              null=True)
    fssai_no = models.CharField(max_length=15, verbose_name=_("FSSAI number"), blank=True, null=True)
    operation_area = models.CharField(verbose_name=_("area of operation"), max_length=200)
    warehouse_image = ProcessedImageField(
        verbose_name=_("shop image"),
        upload_to='auth/warehouse/shop/',
        format='WEBP',
        options={'quality': 50},
        blank=True, null=True,
        help_text=_("Upload warehouse image.")
    )
    warehouse_image_owner = ProcessedImageField(
        verbose_name=_("shop image with owner"),
        upload_to='auth/warehouse/shop_with_owner/',
        format='WEBP',
        options={'quality': 50},
        blank=True, null=True,
        help_text=_("Upload warehouse image with owner.")
    )
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))

    def save(self, *args, **kwargs):
        if not self.warehouse_id:
            last_object = WareHouse.objects.order_by('-id').first()
            if last_object and last_object.warehouse_id:
                last_warehouse_id = last_object.warehouse_id
                warehouse_id_prefix = last_warehouse_id[:-3]
                warehouse_id_suffix = last_warehouse_id[-3:]
                new_suffix = str(int(warehouse_id_suffix) + 1).zfill(3)
                self.warehouse_id = f"{warehouse_id_prefix}{new_suffix}"
            else:
                self.warehouse_id = "WH0001"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"warehouse - {self.name}"

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")


class Customer(User):

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class Driver(User):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name=_("warehouse"))
    address = models.TextField(verbose_name=_("Address"))
    license = models.CharField(verbose_name=_("DL number"), max_length=16)
    license_front = models.ImageField(verbose_name=_("license front image"), upload_to='driver/license')
    license_back = models.ImageField(verbose_name=_("license back image"), upload_to='driver/license')
    aadhar_no = models.CharField(verbose_name=_("Aadhar Number"), max_length=12,
                                 validators=[numeric(_("Aadhar Number")), minimum(12, _("Aadhar number")),
                                             maximum(12, 'Aadhar number')],
                                 help_text=_("Only numbers are allowed."))
    pan_no = models.CharField(verbose_name=_("Pan Number"), max_length=10, validators=[pan_validator], blank=True,
                              null=True)
    aadhar_document = models.FileField(
        verbose_name=_("Aadhar Document"),
        upload_to='driver/aadhar',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        help_text=_("Upload Aadhar card.."), )
    pan_document = models.FileField(
        verbose_name=_("Pan Document"),
        upload_to='driver/pan',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'webp'])],
        help_text=_("Upload Pan card.."), )
    vehicle_no = models.CharField(verbose_name=_("vehicle number"), max_length=10)
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))
    is_free = models.BooleanField(default=True, verbose_name=_("Is Free")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name=_("user"))
    otp = models.CharField(max_length=6,verbose_name=_("OTP"))
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
