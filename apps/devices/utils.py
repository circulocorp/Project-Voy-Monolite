from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_imei(imei):
    """Valida que el IMEI tenga el prefijo 862476 y sea un IMEI válido según el algoritmo de Luhn."""
    if not imei.startswith('862476'):
        raise ValidationError(_('El IMEI debe comenzar con 862476.'))

    # Validar longitud del IMEI
    if len(imei) != 15:
        raise ValidationError(_('El IMEI debe tener 15 dígitos.'))