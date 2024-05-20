from django.contrib import admin
from apps.devices.models import Device
from apps.users.models import User
from apps.devices.forms import DeviceAdminForm


class DeviceAdmin(admin.ModelAdmin):
    form = DeviceAdminForm
    list_display = ('device_id', 'brand', 'model', 'imei', 'assigned_line', 'created_at', 'updated_at')
    search_fields = ('imei', 'assigned_line')
    list_filter = ('brand', 'model')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # No filtramos por request.user aquí, sino mostramos todos los usuarios
            kwargs["queryset"] = User.objects.all()
        # Dejamos que el formulario personalizado filtre profile y vehicle
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Device, DeviceAdmin)
