# Generated by Django 5.0.6 on 2024-06-19 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_is_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accept_terms',
            field=models.BooleanField(default=False, verbose_name='Acepta términos y condiciones'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_terms',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de aceptación de términos y condiciones'),
        ),
    ]
