from django.contrib import admin
from django.urls import path,re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('galltech/admin/doc/', include('django.contrib.admindocs.urls')),
    path('galltech/admin/', admin.site.urls),
    path('provider/', include('provider.urls')),  # Include the accounts app URLs
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'SMS Center - Admin Panel'
