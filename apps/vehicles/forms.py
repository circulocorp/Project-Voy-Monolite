from django import forms
from apps.vehicles.models import Vehicle


class CreateVehicleForm(forms.ModelForm):

    display_name = forms.CharField(
        label='Nombre del vehículo',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    brand = forms.CharField(
        label='Marca del vehículo',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    model = forms.CharField(
        label='Modelo del vehículo',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    year = forms.IntegerField(
        label='Año del vehículo',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    color = forms.CharField(
        label='Color del vehículo',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    serial_number = forms.CharField(
        label='Número de serie/VIN del vehículo',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    plate = forms.CharField(
        label='Placa del vehículo',
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Vehicle
        fields = [
            'display_name',
            'brand',
            'model',
            'year',
            'color',
            'serial_number',
            'plate',
        ]
        labels = {
            'display_name': 'Nombre del vehículo',
            'brand': 'Marca del vehículo',
            'model': 'Modelo del vehículo',
            'year': 'Año del vehículo',
            'color': 'Color del vehículo',
            'serial_number': 'Número de serie/VIN del vehículo',
            'plate': 'Placa del vehículo',
        }
        widgets = {
            'display_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'brand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'year': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'serial_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'plate': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }