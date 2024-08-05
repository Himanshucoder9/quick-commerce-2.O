from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Warehouse.views import (
    TaxListView,
    UnitListView,
    PackagingTypeListView,
    SimpleCategoryViewSet,
    CategoryViewSet
)
router = DefaultRouter()
router.register(r'simple-categories', SimpleCategoryViewSet, basename='simple-category')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('tax-list/', TaxListView.as_view(), name='tax-list'),
    path('unit-list/', UnitListView.as_view(), name='unit-list'),
    path('packaging-type-list/', PackagingTypeListView.as_view(), name='packaging-type-list'),
    
]
