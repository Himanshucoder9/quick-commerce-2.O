from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Warehouse.views import (
    TaxListView,
    UnitListView,
    PackagingTypeListView,
    SimpleCategoryListView,
    CategoryListView,
    SimpleSubCategoryListView,
    SubCategoryListView,
    SimpleAllProductListView,
    AllProductListView,
    ProductDetailView,
    ProductViewSet,
    ProductDisableView, ProductActiveView, PendingOrdersView, AvailableDriverListView,
    DeliveryAssignCreateView, AllWareHouseListView, WarehouseDashboardAPIView, SliderViewSet,
    SliderListView,
    CategoryRetrieveView,
    BulkProductUploadAPIView, ExportProductsAPIView, BulkProductUpdateAPIView
)

# Router configuration for viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'sliders', SliderViewSet, basename='slider')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),

    # Available Warehouse
    path('available/list/', AllWareHouseListView.as_view(), name='warehouse-list'),
    path('dashboard/', WarehouseDashboardAPIView.as_view(), name='dashboard'),

    # Tax and Unit endpoints
    path('tax/list/', TaxListView.as_view(), name='tax-list'),
    path('unit/list/', UnitListView.as_view(), name='unit-list'),
    path('packaging-type/list/', PackagingTypeListView.as_view(), name='packaging-type-list'),

    # Category endpoints
    path('simple-category/list/', SimpleCategoryListView.as_view(), name='simple-categories-list'),
    path('category/list/', CategoryListView.as_view(), name='categories-list'),
    path('category/detail/<str:slug>/', CategoryRetrieveView.as_view(), name='categories-detail'),

    # Subcategory endpoints
    path('simple-subcategory/list/', SimpleSubCategoryListView.as_view(),
         name='simple-subcategory-list'),
    path('subcategory/list/', SubCategoryListView.as_view(), name='subcategory-list'),

    # Product endpoints
    path('simple-products/list/<int:warehouse_id>/', SimpleAllProductListView.as_view(), name='simple-products-list'),
    path('products/list/<int:warehouse_id>/', AllProductListView.as_view(), name='products-list'),

    # Product detail endpoints
    path('product/detail/<str:slug>/proid/<str:sku_no>/', ProductDetailView.as_view(), name='products-detail'),

    # Product management endpoints
    path('products/<str:slug>/proid/<str:sku_no>/',
         ProductViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='product-detail'),
    path('product/disable/<str:slug>/proid/<str:sku_no>/', ProductDisableView.as_view(), name='product-disable'),
    path('product/active/<str:slug>/proid/<str:sku_no>/', ProductActiveView.as_view(), name='product-active'),
    # path('categories/bulk-upload/', CategoryBulkUploadView.as_view(), name='category-bulk-upload'),
    # path('subcategories/bulk-upload/', SubCategoryBulkUploadView.as_view(), name='subcategory-bulk-upload'),
    path('upload/', BulkProductUploadAPIView.as_view(), name='bulk-product-upload'),
    path('bulk/update/', BulkProductUpdateAPIView.as_view(), name='bulk-product-upload'),
    path('export-products/', ExportProductsAPIView.as_view(), name='export-products'),
    # Slider
    path('slider/list/<int:warehouse_id>/', SliderListView.as_view(), name='slider-list'),

    # Delivery
    path('orders/pending/', PendingOrdersView.as_view(), name='pending-orders'),
    path('driver/available/', AvailableDriverListView.as_view(), name='available-drivers'),
    path('driver/assign/', DeliveryAssignCreateView.as_view(), name='assign-driver'),

]
