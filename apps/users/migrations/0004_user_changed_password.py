# Generated by Django 5.0.6 on 2024-05-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='changed_password',
            field=models.BooleanField(default=False, verbose_name='Contraseña cambiada'),
        ),
    ]
