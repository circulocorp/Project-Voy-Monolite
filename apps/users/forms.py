from django import forms
from django.contrib.auth import authenticate
from apps.users.models import ADRESS_TYPES, EmergencyContact, Profile, User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


class RegistrationForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    email_confirmation = forms.EmailField(
        required=True,
        label='Confirmar correo electrónico',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    imei = forms.CharField(
        max_length=15,
        required=True,
        label='Ingresa los 15 dígitos IMEI del dispositivo',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class VerifyRegistrationForm(forms.Form):

    otp = forms.CharField(
        max_length=6,
        required=True,
        label='Contraseña temporal',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class LoginForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        required=True,
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user_obtain: User = User.objects.filter(email=email).first()

        if not user_obtain:
            pass

        if not user_obtain.accept_terms and user_obtain.date_terms:
            raise forms.ValidationError('La cuenta ha sido inhabilitada por no aceptar los alcances de la plataforma. Por favor, contacta a soporte para corregir la situación.')

        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Las credenciales proporcionadas son inválidas.')

        cleaned_data['user'] = user
        return cleaned_data
    

class CreateProfileForm(forms.Form):

    display_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre de perfil',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    names = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre(s)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    pattern_last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellido paterno',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    mattern_last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellido materno',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        max_length=10,
        required=True,
        label='Teléfono celular a 10 dígitos',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    is_owner = forms.BooleanField(
        required=False,
        label='¿El titular de la cuenta puede reportar siniestros?',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    adress = forms.CharField(
        max_length=150,
        required=True,
        label='Dirección',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    ext_number = forms.CharField(
        max_length=10,
        required=True,
        label='Número exterior',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    int_number = forms.CharField(
        max_length=10,
        required=False,
        label='Número interior',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    zip_code = forms.CharField(
        max_length=5,
        required=True,
        label='Código postal',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    state = forms.CharField(
        max_length=150,
        required=True,
        label='Estado',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    city = forms.CharField(
        max_length=150,
        required=True,
        label='Ciudad',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    colony = forms.CharField(
        required=True,
        label='Colonia',
        widget=forms.HiddenInput()
    )

    adress_type = forms.ChoiceField(
        required=True,
        label='Tipo de dirección',
        choices=ADRESS_TYPES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

class UpdateProfileForm(forms.ModelForm):

    display_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre de perfil',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    names = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre(s)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    pattern_last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellido paterno',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    mattern_last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellido materno',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        max_length=10,
        required=True,
        label='Teléfono celular a 10 dígitos',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    adress = forms.CharField(
        max_length=150,
        required=True,
        label='Dirección',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    ext_number = forms.CharField(
        max_length=10,
        required=True,
        label='Número exterior',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    int_number = forms.CharField(
        max_length=10,
        required=False,
        label='Número interior',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    zip_code = forms.CharField(
        max_length=5,
        required=True,
        label='Código postal',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    state = forms.CharField(
        max_length=150,
        required=True,
        label='Estado',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    city = forms.CharField(
        max_length=150,
        required=True,
        label='Ciudad',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    colony = forms.CharField(
        required=True,
        label='Colonia',
        widget=forms.HiddenInput()
    )

    adress_type = forms.ChoiceField(
        required=True,
        label='Tipo de dirección',
        choices=ADRESS_TYPES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )


    class Meta:
        model = Profile
        fields = [
            'display_name',
            'names',
            'pattern_last_name',
            'mattern_last_name',
            'phone',
            'adress',
            'ext_number',
            'int_number',
            'zip_code',
            'state',
            'city',
            'colony',
            'adress_type',
        ]


class EmergencyContactForm(forms.ModelForm):

    complete_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre completo',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        max_length=10,
        required=True,
        label='Teléfono celular a 10 dígitos',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = EmergencyContact
        fields = [
            'complete_name',
            'phone',
            'email',
        ]



class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}),
        help_text='La contraseña actual la encontrarás en el correo de bienvenida que te enviamos al registrarte.'
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        help_text='La contraseña debe contener al menos 8 caracteres, no puede ser similar a su otra información personal y no puede ser una contraseña común.'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)