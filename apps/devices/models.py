from django.db import models
from django.utils.translation import gettext as _
from apps.users.models import User, Profile
from apps.devices.constants import DEVICE_BRAND, DEVICE_MODEL
from apps.devices.utils import validate_imei
from apps.vehicles.models import Vehicle
import uuid


class Device(models.Model):

    # Device Information

    uuid = models.UUIDField(
        _('Identificador único'),
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )

    device_id = models.CharField(
        _('Identificador del dispositivo'),
        max_length=8,
        default='01020300'
    )

    brand = models.CharField(
        _('Marca del dispositivo'),
        max_length=50,
        choices=DEVICE_BRAND,
        default='Cellocator',
    )

    model = models.CharField(
        _('Modelo del dispositivo'),
        max_length=50,
        choices=DEVICE_MODEL,
        default='JIMI VL03',
    )

    imei = models.CharField(
        _('IMEI del dispositivo'),
        max_length=15,
        unique=True,
        validators=[validate_imei],
    )

    assigned_line = models.CharField(
        _('Línea asignada'),
        max_length=10,
    )

    sim_number = models.CharField(
        _('Número de SIM'),
        max_length=19,
    )

    # Device flags

    is_active = models.BooleanField(
        _('Activo'),
        default=False,
    )

    # Device relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='devices',
    )

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='devices_profile',
    )

    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='devices_vehicle',
        blank=True,
        null=True,
    )

    # Device timestamps

    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Dispositivo')
        verbose_name_plural = _('Dispositivos')

    def __str__(self):
        return self.imei
