import os
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from apps.devices.forms import CreateDeviceForm, UpdateDeviceForm
from apps.devices.models import Device
from apps.users.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.vehicles.models import Vehicle
from django.contrib import messages


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'devices/index.html'
    context_object_name = 'devices'

    def get_queryset(self):
        return Device.objects.filter(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos | Voy'
        context['subtitle'] = 'Equipos'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    

class CreateDeviceView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = CreateDeviceForm
    template_name = 'devices/create.html'
    success_url = reverse_lazy('devices:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar equipo | Voy'
        context['subtitle'] = 'Registrar equipo'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user = self.request.user

        available_profiles = Profile.objects.filter(
            user=user,
            devices_profile__isnull=True
        )

        available_vehicles = Vehicle.objects.filter(
            user=user,
            devices_vehicle__isnull=True
        )

        kwargs['available_profiles'] = available_profiles
        kwargs['available_vehicles'] = available_vehicles
        return kwargs

    def form_valid(self, form):
        if form.instance.assigned_line and form.instance.sim_number and form.instance.imei:
                form.instance.is_active = True
        form.instance.user = self.request.user

        user = self.request.user

        if not user.create_device:
            user.create_device = True
            user.save()
            messages.success(self.request, 'Equipo registrado correctamente')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        
        messages.success(self.request, 'Equipo registrado correctamente')
        return super().form_valid(form)
    

class UpdateDeviceView(LoginRequiredMixin, UpdateView):
    model = Device
    form_class = UpdateDeviceForm
    template_name = 'devices/update.html'
    success_url = reverse_lazy('devices:list')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Device.objects.filter(
            user=self.request.user
        )
    
    def form_valid(self, form):
        try:
            if form.instance.assigned_line and form.instance.sim_number and form.instance.imei:
                form.instance.is_active = True

            response = super().form_valid(form)
                
            vehicle_uuid = form.cleaned_data.get('vehicle')
            vehicle = Vehicle.objects.get(uuid=vehicle_uuid)
            form.instance.vehicle = vehicle

            user = self.request.user

            if not user.create_device:
                user.create_device = True
                user.save()
                messages.success(self.request, 'Equipo actualizado correctamente')
                return HttpResponseRedirect(reverse_lazy('users:dashboard'))
            
            messages.success(self.request, 'Equipo actualizado correctamente')
            
            return response
            
        except Exception as e:
            form.add_error(None, e)
            print(e)
            return self.form_invalid(form)
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user = self.request.user

        available_vehicles = Vehicle.objects.filter(
            user=user,
            devices_vehicle__isnull=True
        )

        is_first_device = Device.objects.filter(user=user).count() == 1

        kwargs['available_vehicles'] = available_vehicles
        kwargs['is_first_device'] = is_first_device
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar equipo | Voy'
        context['subtitle'] = 'Actualizar equipo'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'devices/detail.html'
    context_object_name = 'device'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Device.objects.filter(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de equipo | Voy'
        context['subtitle'] = 'Detalle de equipo: {}'.format(self.object.imei)
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context