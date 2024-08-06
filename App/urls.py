
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('auth/', include('Auth.urls')),
    path('general/', include('General.urls')),
    path('customer/', include('Customer.urls')),
    path('warehouse/', include('Warehouse.urls')),
    # path('delivery/', include('Delivery.urls')),
    # path('notification/', include('Notification.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),

    # Spectacular url
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
