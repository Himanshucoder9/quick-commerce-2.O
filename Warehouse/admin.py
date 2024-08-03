from django.contrib import admin
from Warehouse.models import(
    Tax,
    Unit,
    Category,
    SubCategory
)

admin.site.register(Tax)
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(SubCategory)
