from django.urls import path
from apps.vehicles import views

app_name = 'vehicles'

urlpatterns = [
    # Vehicle list
    path('list/', views.VehicleListView.as_view(), name='list'),
    # Create vehicle
    path('create/', views.VehicleCreateView.as_view(), name='create'),
    # Update vehicle
    path('update/<uuid:uuid>/', views.VehicleUpdateView.as_view(), name='update'),
    # Vehicle detail
    path('detail/<uuid:uuid>/', views.VehicleDetailView.as_view(), name='detail'),
]