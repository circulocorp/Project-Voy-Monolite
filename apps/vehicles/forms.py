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
                'placeholder': 'Vehículo',
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
                'placeholder': 'Nissan',
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
                'placeholder': 'Sentra',
            }
        )
    )

    year = forms.IntegerField(
        label='Año del vehículo',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '2020',
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
                'placeholder': 'Rojo',
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
                'placeholder': '1N4BL4BV1LC123456',
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
                'placeholder': 'ABC123',
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
                    'placeholder': 'Vehículo',
                }
            ),
            'brand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nissan',
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Sentra',
                }
            ),
            'year': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '2020',
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Rojo',
                }
            ),
            'serial_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '1N4BL4BV1LC123456',
                }
            ),
            'plate': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ABC123',
                }
            ),
        }