# Generated by Django 5.0.6 on 2024-05-20 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_alter_device_profile'),
        ('users', '0008_profile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='users.profile'),
        ),
    ]
