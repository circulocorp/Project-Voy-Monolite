from django.urls import path
from apps.devices import views


app_name = 'devices'

urlpatterns = [
    # Device list
    path('list/', views.DeviceListView.as_view(), name='list'),
    # Create device
    path('create/', views.CreateDeviceView.as_view(), name='create'),
    # Update device
    path('update/<uuid:uuid>/', views.UpdateDeviceView.as_view(), name='update'),
    # Detail device
    path('detail/<uuid:uuid>/', views.DeviceDetailView.as_view(), name='detail'),
]