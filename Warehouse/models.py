from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field
from Auth.models import WareHouse
from Master.image_uploader import image_with_path
from Master.models import TimeStamp, SEO
from General.models import Country


class Tax(TimeStamp):
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("rate"))

    class Meta:
        verbose_name = _("Tax")
        verbose_name_plural = _("Taxes")

    def __str__(self):
        return f"{self.rate}%"


class Unit(TimeStamp):
    name = models.CharField(verbose_name=_("name"), max_length=20, unique=True,
                            help_text=_("Enter units - kilogram, gram etc."))
    abbreviation = models.CharField(verbose_name=_("abbreviation"), max_length=10, unique=True,
                                    help_text=_("Enter abbreviation - kg, g etc."))

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")

    def __str__(self):
        return self.name


class PackagingType(TimeStamp):
    type = models.CharField(max_length=50, verbose_name=_("Packaging Type"))

    class Meta:
        verbose_name = _("Packaging Type")
        verbose_name_plural = _("Packaging Type")

    def __str__(self):
        return self.type


class Category(TimeStamp):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name=_("warehouse"))
    title = models.CharField(verbose_name=_("category title"), max_length=50, unique=True)
    image = ProcessedImageField(
        upload_to=image_with_path(path="category/image"),
        format="WEBP",
        options={"quality": 50}, verbose_name=_("category image")
    )
    slug = AutoSlugField(populate_from="title", editable=True, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class SubCategory(TimeStamp):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name=_("warehouse"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("category"))
    title = models.CharField(verbose_name="subcategory title", max_length=50, unique=True)
    image = ProcessedImageField(
        upload_to=image_with_path(path="subcategory/image"),
        format="WEBP",
        options={"quality": 50}, verbose_name="subcategory image"
    )
    slug = AutoSlugField(populate_from="title", editable=True, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.title


class Product(SEO, TimeStamp):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name=_("warehouse"))
    sku_no = models.CharField(verbose_name=_("sku no."), max_length=20)
    title = models.CharField(max_length=100, verbose_name=_("product title"))
    size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_("size unit"))
    size = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("size"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("category"))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name=_("subcategory"))

    # Image fields
    image1 = ProcessedImageField(
        upload_to=image_with_path(path="product/images"),
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 1"),
        blank=True, null=True
    )
    image2 = ProcessedImageField(
        upload_to=image_with_path(path="product/images"),
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 2"),
        blank=True, null=True
    )
    image3 = ProcessedImageField(
        upload_to=image_with_path(path="product/images"),
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 3"),
        blank=True, null=True
    )
    image4 = ProcessedImageField(
        upload_to=image_with_path(path="product/images"),
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 4"),
        blank=True, null=True
    )
    image5 = ProcessedImageField(
        upload_to=image_with_path(path="product/images"),
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 5"),
        blank=True, null=True
    )

    # Attribute fields
    attribute_key1 = models.CharField(verbose_name=_("attribute key 1"), max_length=100, blank=True, null=True)
    attribute_value1 = models.TextField(verbose_name=_("attribute value 1"), max_length=100, blank=True, null=True)
    attribute_key2 = models.CharField(verbose_name=_("attribute key 2"), max_length=100, blank=True, null=True)
    attribute_value2 = models.TextField(verbose_name=_("attribute value 2"), max_length=100, blank=True, null=True)
    attribute_key3 = models.CharField(verbose_name=_("attribute key 3"), max_length=100, blank=True, null=True)
    attribute_value3 = models.TextField(verbose_name=_("attribute value 3"), max_length=100, blank=True, null=True)
    attribute_key4 = models.CharField(verbose_name=_("attribute key 4"), max_length=100, blank=True, null=True)
    attribute_value4 = models.TextField(verbose_name=_("attribute value 4"), max_length=100, blank=True, null=True)
    attribute_key5 = models.CharField(verbose_name=_("attribute key 5"), max_length=100, blank=True, null=True)
    attribute_value5 = models.TextField(verbose_name=_("attribute value 5"), max_length=100, blank=True, null=True)
    attribute_key6 = models.CharField(verbose_name=_("attribute key 6"), max_length=100, blank=True, null=True)
    attribute_value6 = models.TextField(verbose_name=_("attribute value 6"), max_length=100, blank=True, null=True)
    attribute_key7 = models.CharField(verbose_name=_("attribute key 7"), max_length=100, blank=True, null=True)
    attribute_value7 = models.TextField(verbose_name=_("attribute value 7"), max_length=100, blank=True, null=True)
    attribute_key8 = models.CharField(verbose_name=_("attribute key 8"), max_length=100, blank=True, null=True)
    attribute_value8 = models.TextField(verbose_name=_("attribute value 8"), max_length=100, blank=True, null=True)

    # Other fields
    country_origin = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,
                                       verbose_name=_("country of origin"))
    packaging_type = models.ForeignKey(PackagingType, max_length=50, on_delete=models.CASCADE)
    description = CKEditor5Field(verbose_name=_("description"), help_text=_("Enter Detailed Description of Product"),
                                  config_name="extends")
    cgst = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("CGST"),
                             related_name="cgst_tax")
    sgst = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("SGST"),
                             related_name="sgst_tax")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_("price"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("discount %"))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_("stock quantity"))
    reorder_level = models.IntegerField(verbose_name=_("reorder level"), default=0)
    is_available = models.BooleanField(default=True, verbose_name=_("product available"))
    is_active = models.BooleanField(default=True, verbose_name=_("product active"))
    slug = AutoSlugField(populate_from="title", editable=True, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.title} - {self.price} Rs."

    def save(self, *args, **kwargs):
        if not any([self.image1, self.image2, self.image3, self.image4, self.image5]):
            self.is_active = False

        self.is_available = self.stock_quantity > 0

        super().save(*args, **kwargs)
