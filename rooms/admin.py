from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Room, RoomInspection, MaintenanceRequest, Building

# Register your models here.
admin.site.register(Room)
admin.site.register(RoomInspection)
admin.site.register(MaintenanceRequest)
admin.site.register(Building)
