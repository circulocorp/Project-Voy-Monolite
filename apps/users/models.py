from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from apps.users.managers import UserManager
import uuid


ADRESS_TYPES = (
    ('D', 'Domicilio particular'),
    ('O', 'Oficina'),
)

class User(AbstractUser):

    # Uuid

    uuid = models.UUIDField(
        _('Identificador único'),
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )

    # User fields

    email = models.EmailField(
        _('Correo electrónico'),
        unique=True,
        blank=False,
        null=False,
    )

    username = models.CharField(
        _('Nombre de usuario'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )

    password = models.CharField(
        _('Contraseña'),
        max_length=128,
        blank=True,
        null=True,
    )

    # Auth fields

    otp = models.CharField(
        _('Código de verificación'),
        max_length=6,
        blank=True,
        null=True,
    )

    otp_expires = models.DateTimeField(
        _('Expiración del código de verificación'),
        blank=True,
        null=True,
    )

    # User flags

    is_verified = models.BooleanField(
        _('Verificado'),
        default=False,
    )

    is_active = models.BooleanField(
        _('Activo'),
        default=False,
    )

    is_staff = models.BooleanField(
        _('Staff'),
        default=False,
    )

    # User steps

    changed_password = models.BooleanField(
        _('Contraseña cambiada'),
        default=False,
    )

    create_profile = models.BooleanField(
        _('Perfil creado'),
        default=False,
    )

    create_vehicle = models.BooleanField(
        _('Vehículo creado'),
        default=False,
    )

    create_emergency_contact = models.BooleanField(
        _('Contacto de emergencia creado'),
        default=False,
    )

    create_device = models.BooleanField(
        _('Dispositivo creado'),
        default=False,
    )

    # Terms and conditions

    accept_terms = models.BooleanField(
        _('Acepta términos y condiciones'),
        default=False,
    )

    date_terms = models.DateTimeField(
        _('Fecha de aceptación de términos y condiciones'),
        blank=True,
        null=True,
    )

    is_superuser = models.BooleanField(
        _('Superusuario'),
        default=False,
    )

    # User dates

    date_joined = models.DateTimeField(
        _('Fecha de registro'),
        auto_now_add=True,
    )

    last_login = models.DateTimeField(
        _('Último acceso'),
        auto_now=True,
    )

    # User manager

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username', )

    objects = UserManager()

    class Meta:
        ordering = ['date_joined']
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return self.email
    
    @property
    def get_username(self):
        return self.email.split('@')[0]
    

# Profile model

class Profile(models.Model):

    # Uuid

    uuid = models.UUIDField(
        _('Identificador único'),
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )

    # Profile fields

    display_name = models.CharField(
        _('Nombre de perfil'),
        max_length=150,
        blank=True,
        null=True,
        unique=False,
    )

    names = models.CharField(
        _('Nombre(s)'),
        max_length=150,
        blank=False,
        null=False,
    )

    pattern_last_name = models.CharField(
        _('Apellido paterno'),
        max_length=150,
        blank=False,
        null=False,
    )

    mattern_last_name = models.CharField(
        _('Apellido materno'),
        max_length=150,
        blank=False,
        null=False,
    )

    phone = models.CharField(
        _('Teléfono celular'),
        max_length=10,
        blank=False,
        null=False,
    )

    is_owner = models.BooleanField(
        _('¿El titular de la cuenta puede reportar siniestros?'),
        default=True,
    )

    adress = models.CharField(
        _('Dirección'),
        max_length=150,
        blank=False,
        null=False,
    )

    ext_number = models.CharField(
        _('Número exterior'),
        max_length=10,
        blank=False,
        null=False,
    )

    int_number = models.CharField(
        _('Número interior'),
        max_length=10,
        blank=True,
        null=True,
    )

    zip_code = models.CharField(
        _('Código postal'),
        max_length=5,
        blank=False,
        null=False,
    )

    state = models.CharField(
        _('Estado'),
        max_length=150,
        blank=False,
        null=False,
    )

    city = models.CharField(
        _('Ciudad'),
        max_length=150,
        blank=False,
        null=False,
    )

    colony = models.CharField(
        _('Colonia'),
        max_length=150,
        blank=False,
        null=False,
    )

    adress_type = models.CharField(
        _('Tipo de dirección'),
        max_length=1,
        choices=ADRESS_TYPES,
        default='D',
    )

    is_active = models.BooleanField(
        _('Activo'),
        default=True,
    )

    # Profile dates

    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True,
    )

    # Profile relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Usuario'),
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfiles')

    def __str__(self):
        return self.display_name
    
    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.email.split('@')[0]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.display_name or self.user.email.split('@')[0]
    

# Emergency contact

class EmergencyContact(models.Model):
    
    # Uuid

    uuid = models.UUIDField(
        _('Identificador único'),
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )

    # Contact fields

    complete_name = models.CharField(
        _('Nombre completo'),
        max_length=150,
        blank=False,
        null=False,
    )

    phone = models.CharField(
        _('Teléfono celular'),
        max_length=10,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        _('Correo electrónico'),
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        _('Activo'),
        default=True,
    )

    # Contact dates

    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True,
    )

    # Contact relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Usuario'),
    )
