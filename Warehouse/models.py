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
    is_deleted = models.BooleanField(default=False, verbose_name=_("is deleted"))

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
    is_deleted = models.BooleanField(default=False, verbose_name=_("is deleted"))

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.title


class Product(SEO, TimeStamp):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name=_("warehouse"))
    sku_no = models.CharField(verbose_name=_("sku no."), max_length=20, unique=True)
    title = models.CharField(max_length=100, verbose_name=_("product title"))
    size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_("size unit"))
    size = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("size"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("category"))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name=_("subcategory"))

    # Image fields
    image1 = ProcessedImageField(
        upload_to="product/images",
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 1"),
        blank=True, null=True
    )
    image2 = ProcessedImageField(
        upload_to="product/images",
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 2"),
        blank=True, null=True
    )
    image3 = ProcessedImageField(
        upload_to="product/images",
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 3"),
        blank=True, null=True
    )
    image4 = ProcessedImageField(
        upload_to="product/images",
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 4"),
        blank=True, null=True
    )
    image5 = ProcessedImageField(
        upload_to="product/images",
        format="WEBP",
        options={"quality": 50}, verbose_name=_("Image 5"),
        blank=True, null=True
    )

    # Attribute fields
    attribute_key1 = models.CharField(verbose_name=_("attribute key 1"), max_length=100, blank=True, null=True)
    attribute_value1 = CKEditor5Field(verbose_name=_("attribute value 1"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key2 = models.CharField(verbose_name=_("attribute key 2"), max_length=100, blank=True, null=True)
    attribute_value2 = CKEditor5Field(verbose_name=_("attribute value 2"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key3 = models.CharField(verbose_name=_("attribute key 3"), max_length=100, blank=True, null=True)
    attribute_value3 = CKEditor5Field(verbose_name=_("attribute value 3"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key4 = models.CharField(verbose_name=_("attribute key 4"), max_length=100, blank=True, null=True)
    attribute_value4 = CKEditor5Field(verbose_name=_("attribute value 4"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key5 = models.CharField(verbose_name=_("attribute key 5"), max_length=100, blank=True, null=True)
    attribute_value5 = CKEditor5Field(verbose_name=_("attribute value 5"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key6 = models.CharField(verbose_name=_("attribute key 6"), max_length=100, blank=True, null=True)
    attribute_value6 = CKEditor5Field(verbose_name=_("attribute value 6"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key7 = models.CharField(verbose_name=_("attribute key 7"), max_length=100, blank=True, null=True)
    attribute_value7 = CKEditor5Field(verbose_name=_("attribute value 7"), config_name="extends", max_length=100,
                                      blank=True, null=True)
    attribute_key8 = models.CharField(verbose_name=_("attribute key 8"), max_length=100, blank=True, null=True)
    attribute_value8 = CKEditor5Field(verbose_name=_("attribute value 8"), config_name="extends", max_length=100,
                                      blank=True, null=True)

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
    is_deleted = models.BooleanField(default=False, verbose_name=_("is deleted"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.title} - {self.price} Rs."

    def save(self, *args, **kwargs):
        # Generate SKU number if it doesn't exist
        if not self.sku_no:
            last_product = Product.objects.order_by('id').last()
            if last_product:
                last_id = int(last_product.sku_no.split('-')[-1]) if last_product.sku_no else 0
                self.sku_no = f"SKU{last_id + 1:09d}"  # Format SKU as "SKU-00000001", "SKU-00000002", etc.
            else:
                self.sku_no = "SKU000000001"  # Starting SKU

        # Rename images based on SKU
        if self.image1:
            self.image1.name = f"product/images/{self.sku_no}_1.webp"
        if self.image2:
            self.image2.name = f"product/images/{self.sku_no}_2.webp"
        if self.image3:
            self.image3.name = f"product/images/{self.sku_no}_3.webp"
        if self.image4:
            self.image4.name = f"product/images/{self.sku_no}_4.webp"
        if self.image5:
            self.image5.name = f"product/images/{self.sku_no}_5.webp"

        # Update availability based on stock quantity
        self.is_available = self.stock_quantity > 0
        self.is_active = self.is_active if any(
            [self.image1, self.image2, self.image3, self.image4, self.image5]) else False

        super().save(*args, **kwargs)
