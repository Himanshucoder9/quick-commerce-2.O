# import os
# import csv
# import io
from datetime import timedelta
# import openpyxl
# from django.utils.text import slugify
# import requests
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Auth.models import WareHouse, Driver
from Customer.models import Order, OrderItem
from Delivery.models import DeliveryAddress
from Warehouse.serializers import (
    TaxSerializer, UnitSerializer, PackagingTypeSerializer, CategorySerializer,
    SimpleSubCategorySerializer, SubCategorySerializer, SimpleProductSerializer,
    ProductSerializer, DetailProductSerializer,
    FullProductSerializer, ProductDisableSerializer,
    PendingOrderSerializer, AvailableDriverSerializer, DeliveryCreateSerializer, AllWarehouseSerializer,
    SliderSerializer
)
from Warehouse.models import Tax, Unit, PackagingType, Category, SubCategory, Product, Slider


class AllWareHouseListView(ListAPIView):
    serializer_class = AllWarehouseSerializer

    def get_queryset(self):
        return WareHouse.objects.filter(approved=True, is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No warehouse available."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaxListView(ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class UnitListView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class PackagingTypeListView(ListAPIView):
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer


class SliderListView(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        warehouse_id = self.kwargs.get('warehouse_id')
        return Slider.objects.filter(warehouse=warehouse_id)


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


class AllProductListView(ListAPIView):
    serializer_class = ProductSerializer

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


class ProductDetailView(RetrieveAPIView):
    serializer_class = DetailProductSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        sku_no = self.kwargs.get('sku_no')
        queryset = Product.objects.filter(slug=slug, sku_no=sku_no, is_deleted=False)

        if not queryset.exists():
            raise NotFound("Product not found.")

        return queryset


# Admin ViewSets
class BaseModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return Response(
            {"detail": f"{self.queryset.model.__name__} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_create(self, serializer):
        serializer.save(warehouse=self.request.user.warehouse)  # Save with warehouse

    def perform_update(self, serializer):
        serializer.save(warehouse=self.request.user.warehouse)


class SliderViewSet(ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_object(self):
        try:
            return self.queryset.get(warehouse=self.request.user.warehouse)
        except self.queryset.model.DoesNotExist:
            raise NotFound(f"Slider not found.")


class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.all()
    serializer_class = FullProductSerializer
    lookup_field = "slug"

    def get_object(self):
        slug = self.kwargs.get('slug')
        sku_no = self.kwargs.get('sku_no')
        try:
            return Product.objects.get(warehouse=self.request.user, slug=slug, sku_no=sku_no, is_deleted=False)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Product updated successfully.", "data": serializer.data})


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
            warehouse = request.user
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
            warehouse = request.user.warehouse_user

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
# class CategoryBulkUploadView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         # Check if a file is provided
#         if 'file' not in request.FILES:
#             return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
#
#         file = request.FILES['file']
#         data = []
#
#         # Define expected column names
#         expected_columns = ['title', 'image_url']
#
#         # Handle CSV files
#         if file.name.endswith('.csv'):
#             decoded_file = file.read().decode('utf-8')
#             io_string = io.StringIO(decoded_file)
#             reader = csv.DictReader(io_string)
#
#             # Validate columns
#             if reader.fieldnames != expected_columns:
#                 return Response(
#                     {"error": f"Invalid CSV columns. Expected: {expected_columns}, Got: {reader.fieldnames}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             for row in reader:
#                 for field in expected_columns:
#                     if field not in row or not row[field]:
#                         return Response(
#                             {"error": f"Missing or empty required field '{field}' in CSV."},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )
#                 data.append(row)
#
#         # Handle Excel files
#         elif file.name.endswith('.xlsx'):
#             workbook = openpyxl.load_workbook(file)
#             sheet = workbook.active
#
#             # Validate column names in the header row
#             header = [cell.value for cell in sheet[1]]  # Read header row
#             if header != expected_columns:
#                 return Response(
#                     {"error": f"Invalid Excel columns. Expected: {expected_columns}, Got: {header}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             for row in sheet.iter_rows(min_row=2, values_only=True):
#                 row_data = dict(zip(header, row))
#                 for field in expected_columns:
#                     if field not in row_data or not row_data[field]:
#                         return Response(
#                             {"error": f"Missing or empty required field '{field}' in Excel."},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )
#                 data.append(row_data)
#         else:
#             return Response({"error": "Unsupported file format. Only .csv and .xlsx are allowed."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Get the warehouse instance for the authenticated user
#         try:
#             warehouse = WareHouse.objects.get(id=request.user.id)
#         except WareHouse.DoesNotExist:
#             return Response({"error": "Authenticated user does not have an associated warehouse."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Prepare to bulk create or update categories
#         categories_to_create = []
#         categories_to_update = []
#         response_data = []
#
#         for item in data:
#             slug = slugify(item['title'])
#             image_name = f"{slug}.webp"  # Use appropriate image extension
#             image_path = f"category/image/{image_name}"
#
#             # Download the image from the provided URL
#             try:
#                 response = requests.get(item['image_url'])
#                 response.raise_for_status()  # Raise an error for bad responses
#
#                 # Save the image to the default storage
#                 image_content = ContentFile(response.content)
#                 image_file_name = default_storage.save(image_path, image_content)  # Save image to media directory
#             except Exception as e:
#                 return Response({"error": f"Failed to download image from {item['image_url']}: {str(e)}"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Prepare category data for bulk create or update
#             category_data = {
#                 'title': item['title'],
#                 'warehouse': warehouse,
#                 'image': image_file_name,
#                 'slug': slug,
#                 'is_deleted': False
#             }
#
#             # Check if the category already exists
#             try:
#                 category = Category.objects.get(title=item['title'], warehouse=warehouse)
#
#                 # If the category exists, prepare it for update
#                 category_data['id'] = category.id
#                 categories_to_update.append(category_data)
#             except Category.DoesNotExist:
#                 # If it doesn't exist, prepare it for creation
#                 categories_to_create.append(category_data)
#
#         # Perform bulk create
#         if categories_to_create:
#             try:
#                 created_categories = Category.objects.bulk_create(
#                     [Category(**data) for data in categories_to_create]
#                 )
#                 for category in created_categories:
#                     response_data.append({
#                         'id': category.id,
#                         'warehouse': category.warehouse.id,
#                         'title': category.title,
#                         'image': category.image.url,
#                         'slug': category.slug,
#                         'created_at': category.created_at,
#                         'updated_at': category.updated_at
#                     })
#             except Exception as e:
#                 return Response({"error": f"Error during bulk creation: {str(e)}"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         # Perform bulk update
#         if categories_to_update:
#             try:
#                 for category_data in categories_to_update:
#                     category = Category.objects.get(id=category_data['id'])
#
#                     # Delete the old image if it exists
#                     if category.image:
#                         old_image_path = category.image.path
#                         if os.path.exists(old_image_path):
#                             os.remove(old_image_path)  # Delete the old image file
#
#                     # Update category fields
#                     category.image = category_data['image']
#                     category.slug = category_data['slug']
#                     category.is_deleted = category_data['is_deleted']
#                     category.save()  # Save the updated category
#
#                     # Add to response data
#                     response_data.append({
#                         'id': category.id,
#                         'warehouse': category.warehouse.id,
#                         'title': category.title,
#                         'image': category.image.url,
#                         'slug': category.slug,
#                         'created_at': category.created_at,
#                         'updated_at': category.updated_at
#                     })
#             except Exception as e:
#                 return Response({"error": f"Error during bulk update: {str(e)}"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         # Return a JSON response with the processed data
#         return Response({"message": "Categories processed successfully.", "data": response_data},
#                         status=status.HTTP_200_OK)
#
#
# class SubCategoryBulkUploadView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         # Check if a file is provided
#         if 'file' not in request.FILES:
#             return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
#
#         file = request.FILES['file']
#         data = []
#
#         # Define expected column names
#         expected_columns = ['title', 'category_id', 'image_url']
#
#         # Handle CSV files
#         if file.name.endswith('.csv'):
#             decoded_file = file.read().decode('utf-8')
#             io_string = io.StringIO(decoded_file)
#             reader = csv.DictReader(io_string)
#
#             # Validate columns
#             if reader.fieldnames != expected_columns:
#                 return Response(
#                     {"error": f"Invalid CSV columns. Expected: {expected_columns}, Got: {reader.fieldnames}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             for row in reader:
#                 for field in expected_columns:
#                     if field not in row or not row[field]:
#                         return Response(
#                             {"error": f"Missing or empty required field '{field}' in CSV."},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )
#                 data.append(row)
#
#         # Handle Excel files
#         elif file.name.endswith('.xlsx'):
#             workbook = openpyxl.load_workbook(file)
#             sheet = workbook.active
#
#             # Validate column names in the header row
#             header = [cell.value for cell in sheet[1]]  # Read header row
#             if header != expected_columns:
#                 return Response(
#                     {"error": f"Invalid Excel columns. Expected: {expected_columns}, Got: {header}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#             for row in sheet.iter_rows(min_row=2, values_only=True):
#                 row_data = dict(zip(header, row))
#                 for field in expected_columns:
#                     if field not in row_data or not row_data[field]:
#                         return Response(
#                             {"error": f"Missing or empty required field '{field}' in Excel."},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )
#                 data.append(row_data)
#         else:
#             return Response({"error": "Unsupported file format. Only .csv and .xlsx are allowed."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Get the warehouse instance for the authenticated user
#         try:
#             warehouse = WareHouse.objects.get(id=request.user.id)
#         except WareHouse.DoesNotExist:
#             return Response({"error": "Authenticated user does not have an associated warehouse."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Prepare to bulk create or update subcategories
#         subcategories_to_create = []
#         subcategories_to_update = []
#         response_data = []
#
#         for item in data:
#             slug = slugify(item['title'])
#             image_name = f"{slug}.webp"  # Use appropriate image extension
#             image_path = f"subcategory/image/{image_name}"
#
#             # Download the image from the provided URL
#             try:
#                 response = requests.get(item['image_url'])
#                 response.raise_for_status()  # Raise an error for bad responses
#
#                 # Save the image to the default storage
#                 image_content = ContentFile(response.content)
#                 image_file_name = default_storage.save(image_path, image_content)  # Save image to media directory
#             except Exception as e:
#                 return Response({"error": f"Failed to download image from {item['image_url']}: {str(e)}"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Prepare subcategory data
#             subcategory_data = {
#                 'title': item['title'],
#                 'warehouse': warehouse,
#                 'image': image_file_name,
#                 'slug': slug,
#                 'is_deleted': False,
#                 'category': None  # Placeholder for category, will set below
#             }
#
#             # Check if the category exists
#             try:
#                 category = Category.objects.get(id=item['category_id'], warehouse=warehouse)
#                 subcategory_data['category'] = category  # Set the category for creation
#
#                 # Check if the subcategory already exists
#                 try:
#                     subcategory = SubCategory.objects.get(title=item['title'], warehouse=warehouse, category=category)
#
#                     # If the subcategory exists, prepare it for update
#                     subcategory.image = image_file_name
#                     subcategory.slug = slug
#                     subcategory.is_deleted = False  # Reset is_deleted to False
#                     subcategory.save()
#                     response_data.append({
#                         'id': subcategory.id,
#                         'warehouse': subcategory.warehouse.id,
#                         'category': subcategory.category.id,
#                         'title': subcategory.title,
#                         'image': subcategory.image.url,
#                         'slug': subcategory.slug,
#                         'created_at': subcategory.created_at,
#                         'updated_at': subcategory.updated_at
#                     })
#
#                 except SubCategory.DoesNotExist:
#                     # If it doesn't exist, prepare it for creation
#                     subcategories_to_create.append(subcategory_data)
#
#             except Category.DoesNotExist:
#                 return Response(
#                     {"error": f"Category with id '{item['category_id']}' does not exist."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#
#         # Perform bulk create for new subcategories
#         if subcategories_to_create:
#             try:
#                 created_subcategories = SubCategory.objects.bulk_create(
#                     [SubCategory(**data) for data in subcategories_to_create]
#                 )
#                 for subcategory in created_subcategories:
#                     response_data.append({
#                         'id': subcategory.id,
#                         'warehouse': subcategory.warehouse.id,
#                         'category': subcategory.category.id,
#                         'title': subcategory.title,
#                         'image': subcategory.image.url,
#                         'slug': subcategory.slug,
#                         'created_at': subcategory.created_at,
#                         'updated_at': subcategory.updated_at
#                     })
#             except Exception as e:
#                 return Response({"error": f"Error during bulk creation: {str(e)}"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         # Return a JSON response with the processed data
#         return Response({"message": "Subcategories processed successfully.", "data": response_data},
#                         status=status.HTTP_200_OK)
