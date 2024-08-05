from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from Warehouse.serializers import (
    TaxSerializer,
    UnitSerializer,
    PackagingTypeSerializer,
    CategorySerializer,
    SimpleSubCategorySerializer
)
from Warehouse.models import(
    Tax,
    Unit,
    PackagingType,
    Category,
    SubCategory
)
class TaxListView(ListAPIView):
    serializer_class = TaxSerializer

    def get_queryset(self):
        return Tax.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No taxes found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UnitListView(ListAPIView):
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No units found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PackagingTypeListView(ListAPIView):
    serializer_class = PackagingTypeSerializer

    def get_queryset(self):
        return PackagingType.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No packaging type found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SimpleCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'message': 'No categories available.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    http_method_names = ['get']
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for category in response.data:
            category['subcategories'] = SimpleSubCategorySerializer(
                SubCategory.objects.filter(category_id=category['id']),
                many=True, context={'request': request}
            ).data
        return response