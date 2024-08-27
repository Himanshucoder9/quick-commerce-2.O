# import csv
# import io
import os
import requests
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
import uuid
import pandas as pd
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Auth.models import WareHouse, Driver
from Customer.models import Order, OrderItem
from Delivery.models import DeliveryAddress
from General.models import Country
from Warehouse.serializers import (
    TaxSerializer, UnitSerializer, PackagingTypeSerializer, CategorySerializer,
    SimpleSubCategorySerializer, SubCategorySerializer, SimpleProductSerializer,
    ProductSerializer, DetailProductSerializer,
    FullProductSerializer, ProductDisableSerializer,
    PendingOrderSerializer, AvailableDriverSerializer, DeliveryCreateSerializer, AllWarehouseSerializer,
    SliderSerializer
)
from Warehouse.models import Tax, Unit, PackagingType, Category, SubCategory, Product, Slider
from django_filters import rest_framework as filters


class AllWareHouseListView(ListAPIView):
    serializer_class = AllWarehouseSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city', None)
        queryset = WareHouse.objects.filter(approved=True, is_active=True)

        if city:
            queryset = queryset.filter(city__name__iexact=city)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No warehouse available."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaxListView(ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No data available."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UnitListView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No data available."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PackagingTypeListView(ListAPIView):
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No data available."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SliderListView(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        warehouse_id = self.kwargs.get('warehouse_id')
        queryset = Slider.objects.filter(warehouse_id=warehouse_id)

        warehouse_id = self.kwargs.get('warehouse_id')
        warehouse = WareHouse.objects.filter(id=warehouse_id)

        if not warehouse.exists():
            raise NotFound("No warehouse found.")

        if not queryset.exists():
            raise NotFound("Product not found.")

        return queryset


class SimpleCategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        for category in response.data:
            category['subcategories'] = SimpleSubCategorySerializer(
                SubCategory.objects.filter(category_id=category['id'], is_deleted=False),
                many=True, context={'request': request}
            ).data
        return response


class CategoryRetrieveView(RetrieveAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        category = response.data
        category['subcategories'] = SimpleSubCategorySerializer(
            SubCategory.objects.filter(category_id=category['id']),
            many=True, context={'request': request}
        ).data
        return response


class SimpleSubCategoryListView(ListAPIView):
    serializer_class = SimpleSubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.filter(is_deleted=False)


class SubCategoryListView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.filter(is_deleted=False)


class SimpleAllProductListView(ListAPIView):
    serializer_class = SimpleProductSerializer

    def get_queryset(self):
        warehouse_id = self.kwargs.get('warehouse_id')
        queryset = Product.objects.filter(warehouse_id=warehouse_id, is_deleted=False)

        warehouse_id = self.kwargs.get('warehouse_id')
        warehouse = WareHouse.objects.filter(id=warehouse_id)

        if not warehouse.exists():
            raise NotFound("No warehouse found.")

        if not queryset.exists():
            raise NotFound("Product not found.")

        return queryset


class ProductListFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {'subcategory': ['exact']}


class AllProductListView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = ProductListFilter
    search_fields = ['title', 'category__title', 'subcategory__title']

    def get_queryset(self):
        warehouse_id = self.kwargs.get('warehouse_id')
        queryset = Product.objects.filter(warehouse_id=warehouse_id, is_deleted=False, is_active=True)

        warehouse_id = self.kwargs.get('warehouse_id')
        warehouse = WareHouse.objects.filter(id=warehouse_id)

        if not warehouse.exists():
            raise NotFound("No warehouse found.")

        if not queryset.exists():
            raise NotFound("Product not found.")

        return queryset


class ProductDetailView(RetrieveAPIView):
    serializer_class = DetailProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        sku_no = self.kwargs.get('sku_no')
        queryset = Product.objects.filter(slug=slug, sku_no=sku_no, is_deleted=False)

        if not queryset.exists():
            raise NotFound("Product not found.")

        return queryset


# Admin ViewSets

class SliderViewSet(ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        queryset = Slider.objects.filter(warehouse=self.request.user.warehouse)
        if not queryset.exists():
            raise NotFound("Slider not found.")
        return queryset

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return self.queryset.get(warehouse=self.request.user.warehouse, pk=pk)
        except self.queryset.model.DoesNotExist:
            raise NotFound(f"Slider not found.")


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = FullProductSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        if not queryset.exists():
            raise NotFound("Product not found.")
        return queryset

    def get_object(self):
        slug = self.kwargs.get('slug')
        sku_no = self.kwargs.get('sku_no')
        try:
            return Product.objects.get(warehouse=self.request.user.warehouse, slug=slug, sku_no=sku_no,
                                       is_deleted=False)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

    def perform_create(self, serializer):
        serializer.save(warehouse=self.request.user.warehouse)

    def perform_update(self, serializer):
        serializer.save(warehouse=self.request.user.warehouse)

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Product updated successfully.", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return Response(
            {"detail": f"{self.queryset.model.__name__} deleted successfully."},
            status=status.HTTP_200_OK
        )


class ProductDisableView(APIView):
    permission_classes = [IsAuthenticated]

    def get_product(self, slug, sku_no, user):
        try:
            return Product.objects.get(slug=slug, sku_no=sku_no, warehouse=user)
        except Product.DoesNotExist:
            return None

    def patch(self, request, slug, sku_no):
        product = self.get_product(slug, sku_no, request.user)
        if product:
            product.is_active = False
            product.save()
            serializer = ProductDisableSerializer(product)
            return Response({"message": "Product disabled successfully.", "product": serializer.data})
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class ProductActiveView(APIView):
    permission_classes = [IsAuthenticated]

    def get_product(self, slug, sku_no, user):
        try:
            return Product.objects.get(slug=slug, sku_no=sku_no, warehouse=user)
        except Product.DoesNotExist:
            return None

    def patch(self, request, slug, sku_no):
        product = self.get_product(slug, sku_no, request.user)
        if product:
            product.is_active = True
            product.save()
            serializer = ProductDisableSerializer(product)
            return Response({"message": "Product active successfully.", "product": serializer.data})
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


# Delivery

class PendingOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            warehouse = request.user.warehouse
        except WareHouse.DoesNotExist:
            return Response({"message": "Warehouse does not exist for this user."}, status=status.HTTP_400_BAD_REQUEST)

        pending_orders = Order.objects.filter(order_status='pending', items__warehouse=warehouse).distinct()

        if not pending_orders:
            return Response({"message": "No orders available for this warehouse."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PendingOrderSerializer(pending_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailableDriverListView(ListAPIView):
    serializer_class = AvailableDriverSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        warehouse = self.request.user.warehouse
        try:
            warehouse = warehouse
        except AttributeError:
            return Driver.objects.none()

        queryset = Driver.objects.filter(warehouse_assigned=warehouse, is_free=True, approved=True, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No drivers available"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryAssignCreateView(CreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        order_ids = data.get('orders')
        driver_id = data.get('driver')

        if not isinstance(order_ids, list) or not order_ids:
            return Response({"message": "A list of order IDs must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        pending_orders = Order.objects.filter(id__in=order_ids, order_status='Pending')
        if pending_orders.count() != len(order_ids):
            return Response({"message": "One or more orders are not pending or do not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            driver = Driver.objects.get(id=driver_id, is_free=True, approved=True)
        except Driver.DoesNotExist:
            return Response({"message": "Driver is not available or not approved"}, status=status.HTTP_400_BAD_REQUEST)

        # Update order status to "Processing"
        pending_orders.update(order_status='Processing')

        # Create the delivery address instance
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            delivery_address = serializer.save()
            delivery_address.orders.set(pending_orders)
            driver.is_free = False
            driver.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Dashboard
class WarehouseDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            warehouse = request.user.warehouse

            # Fetch all products and order items for the warehouse
            products = Product.objects.filter(warehouse=warehouse)
            order_items = OrderItem.objects.filter(warehouse=warehouse)

            # Calculate metrics
            total_products = products.count()
            total_orders = order_items.count()
            completed_order_items = order_items.filter(order__payment__payment_status='Completed')

            total_revenue = self.calculate_total_revenue(completed_order_items)
            todays_orders_count, todays_revenue = self.calculate_today_metrics(completed_order_items)
            past_7_days_orders_count = self.calculate_past_days_metrics(completed_order_items, days=7)
            this_months_orders_count, this_months_revenue = self.calculate_month_metrics(completed_order_items)

            # Count pending and completed orders
            pending_orders_count = self.count_orders(warehouse, order_status='pending')
            completed_orders_count = self.count_orders(warehouse, order_status='completed')

            return Response({
                "total_products": total_products,
                "total_orders": total_orders,
                "todays_orders_count": todays_orders_count,
                "past_7_days_orders_count": past_7_days_orders_count,
                "this_months_orders_count": this_months_orders_count,
                "total_revenue": total_revenue,
                "todays_revenue": todays_revenue,
                "this_months_revenue": this_months_revenue,
                "pending_orders_count": pending_orders_count,
                "completed_orders_count": completed_orders_count,
            }, status=status.HTTP_200_OK)

        except WareHouse.DoesNotExist:
            return Response({"detail": "Warehouse profile not found for this user"}, status=status.HTTP_404_NOT_FOUND)

    def calculate_total_revenue(self, completed_order_items):
        """Calculate total revenue from completed order items."""
        return sum(item.item_price for item in completed_order_items)

    def calculate_today_metrics(self, completed_order_items):
        """Calculate today's orders count and revenue."""
        today = now().date()
        today_orders = completed_order_items.filter(order__created_at__date=today)
        todays_revenue = sum(item.item_price for item in today_orders)
        return today_orders.count(), todays_revenue

    def calculate_past_days_metrics(self, completed_order_items, days):
        """Calculate the number of orders in the past specified number of days."""
        last_days = now() - timedelta(days=days)
        return completed_order_items.filter(order__created_at__gte=last_days).count()

    def calculate_month_metrics(self, completed_order_items):
        """Calculate orders count and revenue for the current month."""
        this_month_start = now().replace(day=1)
        this_month_orders = completed_order_items.filter(order__created_at__gte=this_month_start)
        return this_month_orders.count(), sum(item.item_price for item in this_month_orders)

    def count_orders(self, warehouse, order_status):
        """Count orders for the given warehouse and status."""
        return Order.objects.filter(order_status=order_status, items__warehouse=warehouse).distinct().count()


# Bulk
class BulkProductUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Determine file type
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension in ['.xls', '.xlsx']:
                df = pd.read_excel(file)
            elif file_extension == '.csv':
                df = pd.read_csv(file)
            else:
                return Response({"error": "Unsupported file format."}, status=status.HTTP_400_BAD_REQUEST)

            # Get the warehouse associated with the authenticated user
            warehouse = WareHouse.objects.get(id=request.user.warehouse.id)

            # Process each row in the DataFrame
            for _, row in df.iterrows():
                # Retrieve or generate SKU
                sku_no = row.get('sku_no') or self.generate_sku()

                # Get other foreign key relationships by ID
                try:
                    size_unit = Unit.objects.get(id=row['size_unit'])
                    category = Category.objects.get(id=row['category'])
                    subcategory = SubCategory.objects.get(id=row['subcategory'])
                    country_origin = Country.objects.get(id=row['country_origin']) if row.get(
                        'country_origin') else None
                    packaging_type = PackagingType.objects.get(id=row['packaging_type'])
                    cgst = Tax.objects.get(id=row['cgst']) if row.get('cgst') else None
                    sgst = Tax.objects.get(id=row['sgst']) if row.get('sgst') else None
                except (Unit.DoesNotExist, Category.DoesNotExist, SubCategory.DoesNotExist,
                        Country.DoesNotExist, PackagingType.DoesNotExist, Tax.DoesNotExist) as e:
                    return Response({"error": f"Invalid foreign key reference: {str(e)}"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Download images from URLs or set to None if not present
                image_fields = {}
                for i in range(1, 6):
                    image_url = row.get(f'image{i}')
                    if pd.notna(image_url):  # Check if the URL is not NaN
                        try:
                            image_content = requests.get(image_url).content
                            image_name = f"{sku_no}_{i}.webp"
                            image_fields[f'image{i}'] = ContentFile(image_content, image_name)
                        except requests.RequestException:
                            image_fields[f'image{i}'] = None
                    else:
                        image_fields[f'image{i}'] = None

                # Create or update the product
                product = Product(
                    warehouse=warehouse,
                    sku_no=sku_no,
                    title=row['title'],
                    size_unit=size_unit,
                    size=row['size'],
                    category=category,
                    subcategory=subcategory,
                    country_origin=country_origin,
                    packaging_type=packaging_type,
                    description=row.get('description'),
                    cgst=cgst,
                    sgst=sgst,
                    price=row['price'],
                    discount=row.get('discount', 0),  # Set default value for optional fields
                    stock_quantity=row['stock_quantity'],
                    stock_unit=size_unit,
                    reorder_level=row.get('reorder_level', 0),  # Set default value for optional fields
                    exp_date=row.get('exp_date')
                )

                # Set image fields to None if no image is provided or if download fails
                for field, image in image_fields.items():
                    setattr(product, field, image)

                # Set slug and availability based on stock quantity
                product.slug = slugify(product.title)
                product.is_available = product.stock_quantity > 0
                product.is_active = any(
                    [getattr(product, f'image{i}') for i in range(1, 6)]
                )

                product.save()

            return Response({"message": "Products uploaded successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def generate_sku(self):
        last_product = Product.objects.order_by("-id").first()
        if last_product and last_product.sku_no:
            last_id = int(last_product.sku_no.replace("SKU", "")) if last_product.sku_no.startswith("SKU") else 0
            return f"SKU{str(last_id + 1).zfill(9)}"
        return "SKU000000001"


class BulkProductUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Determine file type
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension in ['.xls', '.xlsx']:
                df = pd.read_excel(file)
            elif file_extension == '.csv':
                df = pd.read_csv(file)
            else:
                return Response({"error": "Unsupported file format."}, status=status.HTTP_400_BAD_REQUEST)

            # Process each row in the DataFrame
            for _, row in df.iterrows():
                # Retrieve SKU to find the existing product
                sku_no = row.get('sku_no')
                if not sku_no:
                    return Response({"error": "SKU number is required for updates."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Try to retrieve the product
                try:
                    product = Product.objects.get(sku_no=sku_no)
                except Product.DoesNotExist:
                    return Response({"error": f"Product with SKU '{sku_no}' does not exist."},
                                    status=status.HTTP_404_NOT_FOUND)

                # Update product fields
                product.title = row.get('title', product.title)
                product.size = row.get('size', product.size)
                product.stock_quantity = row.get('stock_quantity', product.stock_quantity)
                product.price = row.get('price', product.price)
                product.discount = row.get('discount', product.discount)
                product.reorder_level = row.get('reorder_level', product.reorder_level)

                # Handle the expiration date carefully
                exp_date = row.get('exp_date')
                if pd.notna(exp_date):
                    product.exp_date = pd.to_datetime(exp_date, errors='coerce')  # Coerce errors to NaT
                else:
                    product.exp_date = None  # Set to None if no valid date

                # Optionally update foreign key relationships
                if 'size_unit' in row and pd.notna(row['size_unit']):
                    product.size_unit = Unit.objects.get(id=row['size_unit'])
                if 'category' in row and pd.notna(row['category']):
                    product.category = Category.objects.get(id=row['category'])
                if 'subcategory' in row and pd.notna(row['subcategory']):
                    product.subcategory = SubCategory.objects.get(id=row['subcategory'])
                if 'country_origin' in row and pd.notna(row['country_origin']):
                    product.country_origin = Country.objects.get(id=row['country_origin'])
                if 'packaging_type' in row and pd.notna(row['packaging_type']):
                    product.packaging_type = PackagingType.objects.get(id=row['packaging_type'])
                if 'cgst' in row and pd.notna(row['cgst']):
                    product.cgst = Tax.objects.get(id=row['cgst'])
                if 'sgst' in row and pd.notna(row['sgst']):
                    product.sgst = Tax.objects.get(id=row['sgst'])

                # Download images from URLs or set to None if not present
                for i in range(1, 6):
                    image_url = row.get(f'image{i}')
                    if pd.notna(image_url) and image_url.strip():  # Check if the URL is not NaN and not empty
                        try:
                            image_content = requests.get(image_url).content
                            if not image_content:
                                return Response({"error": f"Image {i} content is empty."},
                                                status=status.HTTP_400_BAD_REQUEST)

                            if self.is_valid_image(image_content):
                                # Create a unique name for the image
                                image_name = f"{sku_no}_{i}_{uuid.uuid4()}.webp"
                                setattr(product, f'image{i}', ContentFile(image_content, image_name))
                            else:
                                return Response({"error": f"Invalid image format for image {i}."},
                                                status=status.HTTP_400_BAD_REQUEST)
                        except requests.RequestException as e:
                            return Response({"error": f"Error downloading image {i}: {str(e)}"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        setattr(product, f'image{i}', None)  # Set to None if no image URL is provided

                # Update slug and availability
                product.slug = slugify(product.title)
                product.is_available = product.stock_quantity > 0
                product.is_active = any(
                    [getattr(product, f'image{i}') for i in range(1, 6)]
                )

                product.save()

            return Response({"message": "Products updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def is_valid_image(self, image_content):
        """ Check if the downloaded content is a valid image. """
        try:
            img = Image.open(BytesIO(image_content))
            img.verify()  # Verify that it is an image
            return True
        except Exception as e:
            print(f"Image validation error: {e}")  # Log the error for debugging
            return False


class ExportProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # Query all products
        products = Product.objects.all()

        # Define the base URL for images
        base_url = 'http://demo.m4bistro.in'  # Change this to your actual domain

        # Create a DataFrame from the queryset
        data = {
            'sku_no': [],
            'title': [],
            'size': [],
            'stock_quantity': [],
            'price': [],
            'discount': [],
            'reorder_level': [],
            'exp_date': [],
            'size_unit': [],
            'category': [],
            'subcategory': [],
            'country_origin': [],
            'packaging_type': [],
            'cgst': [],
            'sgst': [],
            'is_available': [],
            'is_active': [],
            'image1': [],
            'image2': [],
            'image3': [],
            'image4': [],
            'image5': []
        }

        for product in products:
            data['sku_no'].append(product.sku_no)
            data['title'].append(product.title)
            data['size'].append(product.size)
            data['stock_quantity'].append(product.stock_quantity)
            data['price'].append(product.price)
            data['discount'].append(product.discount)
            data['reorder_level'].append(product.reorder_level)
            data['exp_date'].append(product.exp_date)
            data['size_unit'].append(product.size_unit.id if product.size_unit else None)
            data['category'].append(product.category.id if product.category else None)
            data['subcategory'].append(product.subcategory.id if product.subcategory else None)
            data['country_origin'].append(product.country_origin.id if product.country_origin else None)
            data['packaging_type'].append(product.packaging_type.id if product.packaging_type else None)
            data['cgst'].append(product.cgst.id if product.cgst else None)
            data['sgst'].append(product.sgst.id if product.sgst else None)
            data['is_available'].append(product.is_available)
            data['is_active'].append(product.is_active)
            data['image1'].append(self.get_full_image_url(product.image1, base_url))
            data['image2'].append(self.get_full_image_url(product.image2, base_url))
            data['image3'].append(self.get_full_image_url(product.image3, base_url))
            data['image4'].append(self.get_full_image_url(product.image4, base_url))
            data['image5'].append(self.get_full_image_url(product.image5, base_url))

        df = pd.DataFrame(data)

        # Check for format query parameter
        file_format = request.query_params.get('format', 'xlsx')

        if file_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=products.csv'
            df.to_csv(response, index=False)
        else:  # Default to Excel format
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=products.xlsx'
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Products')

        return response

    def get_full_image_url(self, image_field, base_url):
        if image_field and hasattr(image_field, 'url'):
            image_url = image_field.url
            if not image_url.startswith(('http://', 'https://')):
                return f"{base_url}{image_url}"  # Prepend base URL if the image URL is relative
            return image_url  # Return the full URL if it already includes a domain
        return None
