from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Users urls
    path('users/', include('apps.users.urls', namespace='users')),
    # Devices urls
    path('devices/', include('apps.devices.urls', namespace='devices')),
    # Vehicles urls
    path('vehicles/', include('apps.vehicles.urls', namespace='vehicles')),
]
