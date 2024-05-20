import os
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from apps.vehicles.models import Vehicle
from apps.vehicles.forms import CreateVehicleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages


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

        if not user.create_vehicle:
            user.create_vehicle = True
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