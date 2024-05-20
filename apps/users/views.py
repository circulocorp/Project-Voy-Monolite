import os
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, ListView, UpdateView, DetailView, CreateView
from apps.users.models import User, Profile, EmergencyContact
from apps.users.forms import RegistrationForm, VerifyRegistrationForm, LoginForm, CreateProfileForm, UpdateProfileForm, EmergencyContactForm, ChangePasswordForm
from django.urls import reverse_lazy
from apps.users.utils import generate_otp, generate_secure_password
from django.utils import timezone
from apps.devices.models import Device
from apps.mailer.main import Mailer
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages


class UserRegistrationView(FormView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('users:register_success')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        imei = form.cleaned_data['imei']
        password = generate_secure_password()

        find_user = User.objects.filter(email=email).exists()
        find_device = Device.objects.filter(imei=imei).exists()


        if find_user:
            form.add_error('email', 'Este correo electrónico ya está registrado.')
            return self.form_invalid(form)
        
        if find_device:
            form.add_error('imei', 'Este dispositivo ya se encuentra registrado.')
            return self.form_invalid(form)
        
        try:
            user = User.objects.create_client_user(
                email=email,
                password=password,
                otp=generate_otp(),
                otp_expires=timezone.now() + timezone.timedelta(minutes=15),
            )

            profile = Profile.objects.create(
                user=user
            )

            device = Device.objects.create(
                user=user,
                imei=imei,
                profile=profile
            )

            mailer: Mailer = Mailer()

            mailer.send_signup_email(
                email=email,
                otp=user.otp,
                password=password,
                url=self.request.build_absolute_uri(reverse_lazy('users:verify', kwargs={'uuid': user.uuid})),
            )

            self.request.session['registration'] = True
            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, 'Ha ocurrido un error al registrar el usuario.')
            print('Error:', e)
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        print('Formulario inválido:', form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de usuario | Voy'
        return context
    
    
class RegistrationSuccessView(TemplateView):
    template_name = 'progress/success.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('registration', False):
            return redirect('users:register')
        del request.session['registration']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro exitoso | Voy'
        return context
    
class RegistrationVerifyView(FormView):
    template_name = 'verification.html'
    form_class = VerifyRegistrationForm
    success_url = reverse_lazy('users:verify_success')

    def form_valid(self, form):
        otp = form.cleaned_data['otp']
        uuid = self.kwargs.get('uuid')

        try:
            user = User.objects.get(uuid=uuid)
            if user.otp == otp and user.otp_expires > timezone.now():
                user.is_verified = True
                user.is_active = True
                user.otp_expires = None
                user.save()
                self.request.session['verified'] = True
                return super().form_valid(form)
            else:
                form.add_error('otp', 'Código de verificación inválido o expirado.')
                return self.form_invalid(form)
        except User.DoesNotExist:
            form.add_error(None, 'Ha ocurrido un error al verificar el usuario.')
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        try:
            user = User.objects.get(uuid=uuid)
            if user.is_verified:
                return redirect('users:login')
            else:
                return super().dispatch(request, *args, **kwargs)
        except User.DoesNotExist:
            return redirect('users:register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Verificación de cuenta | Voy'
        return context
    
    def form_invalid(self, form):
        print('Formulario inválido:', form.errors)
        return super().form_invalid(form)
    

class VerificationSuccessView(TemplateView):

    template_name = 'progress/verification_success.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('verified', False):
            return redirect('users:register')
        del request.session['verified']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Verificación exitosa | Voy'
        return context
    

# Login and logout views

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión | Voy'
        return context
    
def logout_view(request):
    logout(request)
    return redirect('users:login')


# Dashboard view

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard | Voy'
        context['version'] = os.getenv('VERSION', '1.0.0')
        context['subtitle'] = 'Inicio'
        context['profile'] = Profile.objects.filter(user=self.request.user).first()
        context['device'] = Device.objects.filter(user=self.request.user).first()
        context['devices'] = Device.objects.filter(user=self.request.user)
        return context
    
# Profiles views

class ProfilesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/index.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfiles | Voy'
        context['subtitle'] = 'Listado de perfiles'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
class CreateProfileView(LoginRequiredMixin, FormView):
    template_name = 'profiles/create.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('users:profiles')

    def form_valid(self, form):

        display_name = form.cleaned_data['display_name']
        names = form.cleaned_data['names']
        pattern_last_name = form.cleaned_data['pattern_last_name']
        mattern_last_name = form.cleaned_data['mattern_last_name']
        phone = form.cleaned_data['phone']
        is_owner = form.cleaned_data['is_owner']
        adress = form.cleaned_data['adress']
        ext_number = form.cleaned_data['ext_number']
        int_number = form.cleaned_data['int_number']
        zip_code = form.cleaned_data['zip_code']
        state = form.cleaned_data['state']
        city = form.cleaned_data['city']
        colony = form.cleaned_data['colony']
        adress_type = form.cleaned_data['adress_type']

        try: 
            profile = Profile.objects.create(
                user=self.request.user,
                display_name=display_name,
                names=names,
                pattern_last_name=pattern_last_name,
                mattern_last_name=mattern_last_name,
                phone=phone,
                is_owner=is_owner,
                adress=adress,
                ext_number=ext_number,
                int_number=int_number,
                zip_code=zip_code,
                state=state,
                city=city,
                colony=colony,
                adress_type=adress_type,
            )

            messages.success(self.request, 'Perfil creado correctamente.')

            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, 'Ha ocurrido un error al crear el perfil.')
            print('Error:', e)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear perfil | Voy'
        context['subtitle'] = 'Nuevo perfil'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'profiles/update.html'
    success_url = reverse_lazy('users:profiles')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Profile.objects.filter(
            user=self.request.user
        )
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        user = self.request.user
        if not user.create_profile:
            user.create_profile = True
            user.save()
            messages.success(self.request, 'Perfil actualizado correctamente.')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        
        messages.success(self.request, 'Perfil actualizado correctamente.')

        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar perfil | Voy'
        context['subtitle'] = 'Editar perfil'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Profile.objects.filter(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de perfil | Voy'
        context['subtitle'] = 'Perfil: {}'.format(self.object.display_name)
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    

# Emergency contacts views

class EmergencyContactsView(LoginRequiredMixin, ListView):
    model = EmergencyContact
    template_name = 'emergency_contacts/index.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return EmergencyContact.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contactos de emergencia | Voy'
        context['subtitle'] = 'Listado de contactos'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context


class CreateEmergencyContactView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'emergency_contacts/create.html'
    success_url = reverse_lazy('users:emergency_contacts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        user = self.request.user
        if not user.create_emergency_contact:
            user.create_emergency_contact = True
            user.save()
            messages.success(self.request, 'Contacto de emergencia creado correctamente.')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        
        messages.success(self.request, 'Contacto de emergencia creado correctamente.')
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear contacto de emergencia | Voy'
        context['subtitle'] = 'Nuevo contacto'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
class UpdateEmergencyContactView(LoginRequiredMixin, UpdateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'emergency_contacts/update.html'
    success_url = reverse_lazy('users:emergency_contacts')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return EmergencyContact.objects.filter(
            user=self.request.user
        )
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        user = self.request.user
        if not user.create_emergency_contact:
            user.create_emergency_contact = True
            user.save()
            messages.success(self.request, 'Contacto de emergencia actualizado correctamente.')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        
        messages.success(self.request, 'Contacto de emergencia actualizado correctamente.')
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar contacto de emergencia | Voy'
        context['subtitle'] = 'Editar contacto'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context
    
# User methods API # User methods API

@login_required
@csrf_exempt
def change_password(request):

    if request.method == 'POST':
        user = request.user
        
        if not user:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
        
        password = request.POST.get('password', None)
        if not password:
            return JsonResponse({'error': 'No se ha proporcionado una contraseña.'}, status=400)
        user.set_password(password)
        user.changed_password = True
        user.save()
        return JsonResponse({'message': 'Contraseña actualizada correctamente.'}, status=200)
    

# Password change view

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if not user.changed_password:
            user.changed_password = True
            user.save()
            messages.success(self.request, 'Contraseña actualizada correctamente.')
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        messages.success(self.request, 'Contraseña actualizada correctamente.')
        return response
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambiar contraseña | Voy'
        context['subtitle'] = 'Cambiar contraseña'
        context['version'] = os.getenv('VERSION', '1.0.0')
        return context