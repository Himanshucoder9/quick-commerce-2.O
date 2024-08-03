from rest_framework import serializers

from General.serializers import CountrySerializer
from Warehouse.models import Tax, Unit, PackagingType, Category, SubCategory, Product


# Tax Serializers
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ("id", "rate",)


class FullTaxSerializer(TaxSerializer):
    class Meta(TaxSerializer.Meta):
        fields = "__all__"


# Unit Serializers
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ("id", "name", "abbreviation")


class FullUnitSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        fields = "__all__"


# PackagingType Serializers
class PackagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingType
        fields = ("id", "type",)


class FullPackagingTypeSerializer(PackagingTypeSerializer):
    class Meta(PackagingTypeSerializer.Meta):
        fields = "__all__"


# Category Serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "warehouse", "title", "image", "slug")


class FullCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = "__all__"


# SubCategory Serializers
class SimpleSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "warehouse", "category", "title", "image", "slug")


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ("id", "warehouse", "category", "title", "image", "slug")


class FullSubCategorySerializer(SubCategorySerializer):
    class Meta(SubCategorySerializer.Meta):
        fields = "__all__"


# SubCategory Serializers
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id", "warehouse", "sku_no", "category", "subcategory", "title", "size_unit", "size", "category",
            "subcategory", "image1",
            "image2", "image3" "image4", "image5", "cgst", "sgst", "price", "discount", "stock_quantity",
            "is_available", "slug")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    size_unit = UnitSerializer(read_only=True)
    cgst = TaxSerializer(read_only=True)
    sgst = TaxSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "warehouse", "sku_no", "category", "subcategory", "title", "size_unit", "size", "category",
            "subcategory", "image1", "image2", "image3" "image4", "image5", "cgst", "sgst", "price", "discount",
            "stock_quantity", "is_available", "slug")


class DetailProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    size_unit = UnitSerializer(read_only=True)
    country_origin = CountrySerializer(read_only=True)
    packaging_type = PackagingTypeSerializer(read_only=True)
    cgst = TaxSerializer(read_only=True)
    sgst = TaxSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("is_active", "reorder_level")


class FullProductSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = "__all__"
