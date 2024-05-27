from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('galltech/admin/doc/', include('django.contrib.admindocs.urls')),
    path('galltech/admin/', admin.site.urls),
    path('provider/', include('provider.urls')),  # Include the accounts app URLs
]

admin.site.site_header = 'SMS Center - Admin Panel'