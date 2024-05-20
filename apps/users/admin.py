from django.contrib import admin
from apps.users.models import User, Profile, EmergencyContact

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(EmergencyContact)
