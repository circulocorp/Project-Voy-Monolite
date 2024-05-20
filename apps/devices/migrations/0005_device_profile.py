# Generated by Django 5.0.6 on 2024-05-20 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_device_is_active'),
        ('users', '0008_profile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='users.profile'),
        ),
    ]