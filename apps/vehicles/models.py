import uuid
from django.db import models
from django.utils.translation import gettext as _
from apps.users.models import User


class Vehicle(models.Model):

    # Vehicle Information

    uuid = models.UUIDField(
        _('Identificador único'),
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )

    display_name = models.CharField(
        _('Nombre del vehículo'),
        max_length=50,
        blank=False,
        null=False,
        default='Vehículo'
    )

    brand = models.CharField(
        _('Marca del vehículo'),
        max_length=50,
        blank=False,
        null=False,
    )

    model = models.CharField(
        _('Modelo del vehículo'),
        max_length=50,
        blank=False,
        null=False,
    )

    year = models.PositiveIntegerField(
        _('Año del vehículo'),
        blank=False,
        null=False,
    )

    color = models.CharField(
        _('Color del vehículo'),
        max_length=50,
        blank=False,
        null=False,
    )

    serial_number = models.CharField(
        _('Número de serie/VIN del vehículo'),
        max_length=50,
        blank=False,
        null=False,
    )

    plate = models.CharField(
        _('Placa del vehículo'),
        max_length=10,
        blank=False,
        null=False,
    )

    # Vehicle Relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Usuario'),
        related_name='vehicles',
    )

    # Vehicle Flags

    is_active = models.BooleanField(
        _('Activo'),
        default=True,
    )

    # Vehicle Metadata

    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Vehículo')
        verbose_name_plural = _('Vehículos')
        ordering = ['-created_at']

    def __str__(self):
        return self.display_name


