from django.contrib import admin
from .models import Room, RoomInspectionRequest, MaintenanceRequest, Building, StudentAllocation, RoomReservation, Complaint, VisitorLog
from .models import Payment, RentalAgreement, Bursary
from accounts.models import CustomUser
from accounts.admin import CustomUserAdmin as AccountsCustomUserAdmin  # Import the original CustomUserAdmin

# @admin.action(description='Allocate rooms to accepted students')
# def allocate_rooms(modeladmin, request, queryset):
#     for student in queryset:
#         # Find an available room based on the student's gender
#         available_rooms = Room.objects.filter(
#             building__gender=student.gender,
#             capacity__gt=Room.objects.filter(occupants=student).count()
#         ).order_by('capacity')

#         if available_rooms:
#             room = available_rooms.first()
#             StudentAllocation.objects.create(student=student, room=room)

@admin.action(description='Allocate rooms to accepted students')
def allocate_rooms(modeladmin, request, queryset):
    for student in queryset:
        print(student)
        # Find an available room based on the student's gender
        available_rooms = Room.objects.filter(
            building__gender_type=student.gender,
            capacity__gt=Room.objects.filter(occupants=student).count()
        ).order_by('capacity')

        print(available_rooms)
        if available_rooms:
            room = available_rooms.first()
            room.occupants.add(student)
            StudentAllocation.objects.create(student=student, room=room)
            print("Added to room!")




class CustomUserAdmin(AccountsCustomUserAdmin):  # Inherit from the original CustomUserAdmin
    actions = [allocate_rooms]

# Unregister the original CustomUser admin and register the new one
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Payment)
admin.site.register(Bursary)
admin.site.register(RentalAgreement)
admin.site.register(RoomInspectionRequest)
admin.site.register(MaintenanceRequest)
admin.site.register(StudentAllocation)
admin.site.register(RoomReservation)
admin.site.register(Complaint)
admin.site.register(VisitorLog)
