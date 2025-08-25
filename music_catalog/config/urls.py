"""
Main URL configuration for Music Catalog API project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include('api.v1.urls')),
    
    # API documentation
    path('api/docs/', include_docs_urls(title='Music Catalog API')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)