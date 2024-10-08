from rest_framework import serializers
from Auth.models import Driver, WareHouse
from Auth.serializers import WareHouseDetailSerializer
from Customer.models import Order
from Delivery.models import DeliveryAddress
from General.serializers import CountrySerializer
from Warehouse.models import Tax, Unit, PackagingType, Category, SubCategory, Product, Slider


# import Customer.serializers as customer_serializers

# Base Serializers
class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True


# All Warehouse List
class AllWarehouseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = WareHouse
        fields = (
        "id", "warehouse_no", "warehouse_name", "city", "approved", "is_active", "latitude", "longitude", "city")


# Slider
class SliderSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Slider
        fields = "__all__"


# Tax Serializers
class TaxSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Tax
        fields = ("id", "rate",)


class FullTaxSerializer(TaxSerializer):
    class Meta(TaxSerializer.Meta):
        fields = "__all__"


# Unit Serializers
class UnitSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Unit
        fields = ("id", "name", "abbreviation")


class FullUnitSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        fields = "__all__"


# PackagingType Serializers
class PackagingTypeSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingType
        fields = ("id", "type",)


class FullPackagingTypeSerializer(PackagingTypeSerializer):
    class Meta(PackagingTypeSerializer.Meta):
        fields = "__all__"


# Category Serializers
class CategorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Category
        fields = ("id", "title", "image", "slug")


class FullCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = "__all__"


# SubCategory Serializers
class SimpleSubCategorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = SubCategory
        fields = ("id", "category", "title", "image", "slug")


class SubCategorySerializer(BaseSerializer):
    category = CategorySerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = SubCategory
        fields = ("id", "category", "title", "image", "slug")


class FullSubCategorySerializer(SubCategorySerializer):
    class Meta(SubCategorySerializer.Meta):
        fields = "__all__"


# Product Serializers
class SimpleProductSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Product
        fields = (
            "id", "warehouse", "sku_no", "category", "subcategory", "title", "size_unit", "size",
            "image1", "image2", "image3", "image4", "image5", "cgst", "sgst",
            "price", "discount", "stock_quantity", "is_available", "slug"
        )


class ProductSerializer(BaseSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SimpleSubCategorySerializer(read_only=True)
    size_unit = UnitSerializer(read_only=True)
    cgst = TaxSerializer(read_only=True)
    sgst = TaxSerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Product
        fields = (
            "id", "warehouse", "sku_no", "category", "subcategory", "title", "size_unit", "size",
            "image1", "image2", "image3", "image4", "image5", "cgst", "sgst",
            "price", "discount", "stock_quantity", "is_available", "slug"
        )


class DetailProductSerializer(BaseSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    size_unit = UnitSerializer(read_only=True)
    country_origin = CountrySerializer(read_only=True)
    packaging_type = PackagingTypeSerializer(read_only=True)
    cgst = TaxSerializer(read_only=True)
    sgst = TaxSerializer(read_only=True)
    warehouse = WareHouseDetailSerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Product
        exclude = ("is_active", "reorder_level",)


class FullProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("sku_no",)


class ProductDisableSerializer(BaseSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ("id", "is_active", "slug", "sku_no")


# Delivery
class PendingOrderSerializer(BaseSerializer):
    shipping_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "payment_method", "order_status", "total_amount", "shipping_address", "created_at"
        )

    def get_shipping_address(self, obj):
        from Customer.serializers import ShippingAddressSerializer  # Import here to avoid circular dependency
        return ShippingAddressSerializer(obj.shipping_address).data


class AvailableDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'address', 'vehicle_no', 'is_free', ]


class DeliveryCreateSerializer(serializers.ModelSerializer):
    # orders = customer_serializers.OrderSerializer(many=True)
    class Meta:
        model = DeliveryAddress
        fields = '__all__'

    def create(self, validated_data):
        validated_data['status'] = 'PROCESSING'
        return super().create(validated_data)


# Bulk
class ProductBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        sku_no = validated_data.get('sku_no')
        product, created = Product.objects.update_or_create(sku_no=sku_no, defaults=validated_data)
        return product