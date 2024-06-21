import os
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from apps.devices.forms import CreateDeviceForm, UpdateDeviceForm
from apps.devices.models import Device
from apps.users.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.vehicles.models import Vehicle
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from apps.vehicles.views import validate_vin


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
        context['title'] = 'Vehículos | Voy'
        context['subtitle'] = 'Vehículos'
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
        context['available_vehicles_rp'] = Vehicle.objects.filter(
            user=self.request.user,
            devices_vehicle__isnull=True
        )
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user = self.request.user

        profile = Profile.objects.filter(
            user=user,
        ).first()

        available_vehicles = Vehicle.objects.filter(
            user=user,
            devices_vehicle__isnull=True
        )

        kwargs['available_profile'] = profile
        kwargs['available_vehicles'] = available_vehicles
        return kwargs

    def form_valid(self, form):
        if form.instance.assigned_line and form.instance.sim_number and form.instance.imei:
            form.instance.is_active = True
        
        form.instance.user = self.request.user

        form.instance.profile = form.cleaned_data['profile']

        user = self.request.user
        if not user.create_device:
            user.create_device = True
            user.save()
            messages.success(self.request, 'Equipo registrado correctamente')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        
        messages.success(self.request, 'Equipo registrado correctamente')
        return super().form_valid(form)
    

@login_required
@csrf_protect
def update_device_view(request, uuid):

    if request.method == 'GET':

        device: Device = Device.objects.get(uuid=uuid, user=request.user)

        context = {
            'device': device,
            'title': 'Actualizar equipo | Voy',
        }

        return render(request, 'devices/update.html', context)
    
    if request.method == 'POST':
        try:
            device_uuid = uuid

            # Obtener los datos de 'deviceData' y 'vehicleData'
            device_id = request.POST.get('deviceData[device_id]')
            brand = request.POST.get('deviceData[brand]')
            model = request.POST.get('deviceData[model]')
            imei = request.POST.get('deviceData[imei]')
            assigned_line = request.POST.get('deviceData[assigned_line]')
            sim_number = request.POST.get('deviceData[sim_number]')

            vehicle_name = request.POST.get('vehicleData[vehicle_name]')
            vehicle_brand = request.POST.get('vehicleData[vehicle_brand]')
            vehicle_model = request.POST.get('vehicleData[vehicle_model]')
            vehicle_year = request.POST.get('vehicleData[vehicle_year]')
            vehicle_color = request.POST.get('vehicleData[vehicle_color]')
            vehicle_serial = request.POST.get('vehicleData[vehicle_serial]')
            vehicle_plate = request.POST.get('vehicleData[vehicle_plate]')

            if not validate_vin(vehicle_serial):
                return JsonResponse({
                    'status': 400,
                    'message': 'El número de serie/VIN no es válido',
                    'form': 'vehicle'
                }, status=400)

            # Buscar el dispositivo
            device = get_object_or_404(Device, uuid=device_uuid, user=request.user)

            # Buscar el perfil
            profile = get_object_or_404(Profile, user=request.user)

            # Crear el vehículo
            vehicle = Vehicle.objects.create(
                display_name=vehicle_name,
                brand=vehicle_brand,
                model=vehicle_model,
                year=vehicle_year,
                color=vehicle_color,
                serial_number=vehicle_serial,
                plate=vehicle_plate,
                user=request.user
            )

            # Actualizar el dispositivo
            device.assigned_line = assigned_line
            device.sim_number = sim_number
            device.vehicle = vehicle
            device.profile = profile
            device.user = request.user

            device.save()

            request.user.create_device = True
            request.user.save()

            return JsonResponse({
                'status': 200,
                'message': 'Dispositivo y vehículo actualizados correctamente',
                'device': {
                    'uuid': str(device.uuid),
                    'assigned_line': device.assigned_line,
                    'sim_number': device.sim_number,
                }
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': f'Ocurrió un error: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 400,
        'message': 'Método no permitido'
    }, status=400)


@login_required
@csrf_protect
def create_device_view(request):

    if request.method == 'POST':
        try:

            # Obtener los datos de 'deviceData' y 'vehicleData'
            device_id = request.POST.get('deviceData[device_id]')
            brand = request.POST.get('deviceData[brand]')
            model = request.POST.get('deviceData[model]')
            imei = request.POST.get('deviceData[imei]')
            assigned_line = request.POST.get('deviceData[assigned_line]')
            sim_number = request.POST.get('deviceData[sim_number]')

            vehicle_name = request.POST.get('vehicleData[vehicle_name]')
            vehicle_brand = request.POST.get('vehicleData[vehicle_brand]')
            vehicle_model = request.POST.get('vehicleData[vehicle_model]')
            vehicle_year = request.POST.get('vehicleData[vehicle_year]')
            vehicle_color = request.POST.get('vehicleData[vehicle_color]')
            vehicle_serial = request.POST.get('vehicleData[vehicle_serial]')
            vehicle_plate = request.POST.get('vehicleData[vehicle_plate]')


            if not validate_vin(vehicle_serial):
                return JsonResponse({
                    'status': 400,
                    'message': 'El número de serie/VIN no es válido',
                    'form': 'vehicle'
                }, status=400)

            # Buscar el perfil
            profile = get_object_or_404(Profile, user=request.user)

            
            if Device.objects.filter(imei=imei).exists():
                return JsonResponse({
                    'status': 400,
                    'message': 'El IMEI ingresado ya ha sido registrado',
                    'form': 'device'
                }, status=400)
            
            if len(imei) != 15 or imei.startswith('000000') or not imei.startswith('862476'):
                return JsonResponse({
                    'status': 400,
                    'message': 'El IMEI ingresado no es válido',
                    'form': 'device'
                }, status=400)
            


            # Crear el vehículo
            vehicle = Vehicle.objects.create(
                display_name=vehicle_name,
                brand=vehicle_brand,
                model=vehicle_model,
                year=vehicle_year,
                color=vehicle_color,
                serial_number=vehicle_serial,
                plate=vehicle_plate,
                user=request.user
            )

            device = Device.objects.create(
                device_id=device_id,
                brand=brand,
                model=model,
                imei=imei,
                assigned_line=assigned_line,
                sim_number=sim_number,
                user=request.user,
                profile=profile,
                vehicle=vehicle
            )

            request.user.create_device = True
            request.user.save()

            return JsonResponse({
                'status': 200,
                'message': 'Dispositivo y vehículo registrados correctamente',
                'device': {
                    'uuid': str(device.uuid),
                    'assigned_line': device.assigned_line,
                    'sim_number': device.sim_number,
                }
            }, status=200)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 500,
                'message': f'Ocurrió un error: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 400,
        'message': 'Método no permitido'
    }, status=400)

# class UpdateDeviceView(LoginRequiredMixin, UpdateView):
#     model = Device
#     form_class = UpdateDeviceForm
#     template_name = 'devices/update.html'
#     success_url = reverse_lazy('devices:list')
#     slug_field = 'uuid'
#     slug_url_kwarg = 'uuid'

#     def get_queryset(self):
#         return Device.objects.filter(
#             user=self.request.user
#         )
    
#     def form_valid(self, form):
#         try:
#             if form.instance.assigned_line and form.instance.sim_number and form.instance.imei:
#                 form.instance.is_active = True

#             response = super().form_valid(form)
                
#             vehicle_uuid = form.cleaned_data.get('vehicle')
#             vehicle = Vehicle.objects.get(uuid=vehicle_uuid)
#             form.instance.vehicle = vehicle

#             user = self.request.user

#             if not user.create_device:
#                 user.create_device = True
#                 user.save()
#                 messages.success(self.request, 'Equipo actualizado correctamente')
#                 return HttpResponseRedirect(reverse_lazy('users:dashboard'))
            
#             messages.success(self.request, 'Equipo actualizado correctamente')
            
#             return response
            
#         except Exception as e:
#             form.add_error(None, e)
#             print(e)
#             return self.form_invalid(form)
        
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()

#         user = self.request.user

#         available_vehicles = Vehicle.objects.filter(
#             user=user,
#             devices_vehicle__isnull=True
#         )

#         is_first_device = Device.objects.filter(user=user, is_active=False).count() == 1

#         kwargs['available_vehicles'] = available_vehicles
#         kwargs['is_first_device'] = is_first_device
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Actualizar equipo | Voy'
#         context['subtitle'] = 'Actualizar equipo'
#         context['version'] = os.getenv('VERSION', '1.0.0')
#         context['is_first_device_arg'] = Device.objects.filter(user=self.request.user, is_active=False).count() == 1
#         return context


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