# Generated by Django 5.0.6 on 2024-05-17 05:54

import apps.devices.utils
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Identificador único')),
                ('device_id', models.CharField(default='01020300', max_length=8, verbose_name='Identificador del dispositivo')),
                ('brand', models.CharField(choices=[('Cellocator', 'Cellocator')], default='Cellocator', max_length=50, verbose_name='Marca del dispositivo')),
                ('model', models.CharField(choices=[('JIMI VL03', 'JIMI VL03')], default='JIMI VL03', max_length=50, verbose_name='Modelo del dispositivo')),
                ('imei', models.CharField(max_length=15, unique=True, validators=[apps.devices.utils.validate_imei], verbose_name='IMEI del dispositivo')),
                ('assigned_line', models.CharField(max_length=10, unique=True, verbose_name='Línea asignada')),
                ('sim_number', models.CharField(max_length=19, unique=True, verbose_name='Número de SIM')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dispositivo',
                'verbose_name_plural': 'Dispositivos',
                'ordering': ('-created_at',),
            },
        ),
    ]