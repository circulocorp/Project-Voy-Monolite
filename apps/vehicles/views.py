import os
import re
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from apps.vehicles.models import Vehicle
from apps.vehicles.forms import CreateVehicleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from apps.devices.models import Device


def validate_vin(vin):
    vin_values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7,
        'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }

    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

    vin_regex = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$')

    if not vin_regex.match(vin):
        return False
    
    total = 0
    for i, char in enumerate(vin):
        total += vin_values[char] * weights[i]
    
    check_digit = total % 11
    if check_digit == 10:
        check_digit = 'X'
    else:
        check_digit = str(check_digit)
    
    return check_digit == vin[8]

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/index.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        return Vehicle.objects.filter(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vehículos | Voy'
        context['subtitle'] = 'Vehículos'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = CreateVehicleForm
    template_name = 'vehicles/create.html'
    success_url = reverse_lazy('vehicles:list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        user = self.request.user

        vin = form.instance.serial_number

        if not validate_vin(vin):
            messages.error(self.request, 'El número de serie/VIN no es válido')
            return response

        if not user.create_vehicle:
            user.create_vehicle = True
            vehicle: Vehicle = form.instance
            first_device = Device.objects.filter(user=user).first()
            first_device.vehicle = vehicle
            user.save()
            messages.success(self.request, 'Vehículo registrado correctamente')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        
        messages.success(self.request, 'Vehículo registrado correctamente')

        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Vehículo | Voy'
        context['subtitle'] = 'Registrar Vehículo'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    

class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = CreateVehicleForm
    template_name = 'vehicles/update.html'
    success_url = reverse_lazy('vehicles:list')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Vehicle.objects.filter(
            user=self.request.user
        )
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Vehículo actualizado correctamente')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Vehículo | Voy'
        context['subtitle'] = 'Actualizar Vehículo'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    

class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'vehicles/detail.html'
    context_object_name = 'vehicle'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Vehicle.objects.filter(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Vehículo | Voy'
        context['subtitle'] = 'Detalle del Vehículo: {0} - {1}'.format(self.object.brand, self.object.model)
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context