from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('accounts/', include('Travel_blog.accounts.urls')),
    path('admin/', admin.site.urls),
    path('', include('Travel_blog.app.urls')),
    # Serve media files in production
 #   re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Travel_blog.app.views.error_views.handler404'
