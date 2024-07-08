from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('voy/admin/', admin.site.urls),
    # Users urls
    path('voy/users/', include('apps.users.urls', namespace='users')),
    # Devices urls
    path('voy/devices/', include('apps.devices.urls', namespace='devices')),
    # Vehicles urls
    path('voy/vehicles/', include('apps.vehicles.urls', namespace='vehicles')),
    path('accounts/', include('django.contrib.auth.urls')),
]