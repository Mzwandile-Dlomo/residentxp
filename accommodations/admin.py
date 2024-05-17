from django.contrib import admin
from .models import Room, RoomInspection, MaintenanceRequest, Building

# Register your models here.
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(RoomInspection)
admin.site.register(MaintenanceRequest)
