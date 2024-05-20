from django import forms
from apps.devices.models import Device, DEVICE_BRAND, DEVICE_MODEL
from apps.users.models import Profile
from apps.vehicles.models import Vehicle


class CreateDeviceForm(forms.ModelForm):

    device_id = forms.CharField(
        label='Identificador del dispositivo',
        required=False,
        max_length=8,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '01020300',
            }
        )
    )

    brand = forms.ChoiceField(
        label='Marca',
        required=False,
        choices=DEVICE_BRAND,
        disabled=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    model = forms.ChoiceField(
        label='Modelo',
        required=False,
        choices=DEVICE_MODEL,
        disabled=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    imei = forms.CharField(
        label='IMEI del equipo a 15 dígitos',
        required=True,
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '862476000000000',
            }
        )
    )

    assigned_line = forms.CharField(
        label='Línea asignada a 10 dígitos',
        required=True,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '3123456789',
            }
        )
    )

    sim_number = forms.CharField(
        label='Número de SIM a 19 dígitos',
        required=True,
        max_length=19,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '89014103211118510720',
            }
        )
    )

    profile = forms.ChoiceField(
        label='Asignar perfil al equipo',
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    vehicle = forms.ChoiceField(
        label='Asignar vehículo al equipo',
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Device
        fields = [
            'device_id',
            'brand',
            'model',
            'imei',
            'assigned_line',
            'sim_number',
            'profile',
            'vehicle',
        ]
        widgets = {
            'device_id': forms.HiddenInput(),
            'brand': forms.HiddenInput(),
            'model': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        available_profiles = kwargs.pop('available_profiles', None)
        available_vehicles = kwargs.pop('available_vehicles', None)
        super().__init__(*args, **kwargs)
        if available_profiles:
            self.fields['profile'].choices = [
                (profile.uuid, profile.display_name)
                for profile in available_profiles
            ]
        if available_vehicles:
            self.fields['vehicle'].choices = [
                (vehicle.uuid, vehicle.display_name)
                for vehicle in available_vehicles
           ]



class UpdateDeviceForm(forms.ModelForm):

    device_id = forms.CharField(
        label='Identificador del dispositivo',
        required=True,
        max_length=8,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '01020300',
            }
        )
    )

    brand = forms.ChoiceField(
        label='Marca',
        required=True,
        choices=DEVICE_BRAND,
        disabled=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    model = forms.ChoiceField(
        label='Modelo',
        required=True,
        choices=DEVICE_MODEL,
        disabled=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    imei = forms.CharField(
        label='IMEI del equipo a 15 dígitos',
        required=True,
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '862476000000000',
            }
        )
    )

    assigned_line = forms.CharField(
        label='Línea asignada a 10 dígitos',
        required=False,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '3123456789',
            }
        )
    )

    sim_number = forms.CharField(
        label='Número de SIM a 19 dígitos',
        required=False,
        max_length=19,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '89014103211118510720',
            }
        )
    )


    vehicle = forms.CharField(
        label='Vehículo asignado al equipo',
        required=False,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Device
        fields = [
            'device_id',
            'brand',
            'model',
            'imei',
            'assigned_line',
            'sim_number',
            'vehicle',
        ]

    def __init__(self, *args, **kwargs):
        available_vehicles = kwargs.pop('available_vehicles', None)
        is_first_device = kwargs.pop('is_first_device', None)
        super().__init__(*args, **kwargs)
        if available_vehicles:
            self.fields['vehicle'].choices = [
                (vehicle.uuid, vehicle.display_name)
                for vehicle in available_vehicles
           ]
            
        if not is_first_device:
            self.fields['imei'].disabled = True
            self.fields['assigned_line'].disabled = True
            self.fields['sim_number'].disabled = True
            
class DeviceAdminForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            user = self.instance.user
            self.fields['profile'].queryset = Profile.objects.filter(user=user)
            self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)