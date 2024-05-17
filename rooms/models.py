from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()  

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()  # Total number of students the building can accommodate
    gender_type = models.CharField(
            max_length=10,
            choices=(
                ('unisex', 'Unisex'),
                ('male', 'Male'),
                ('female', 'Female'),
            ),
        )
    
    def __str__(self):
        return self.name


class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    occupants = models.ManyToManyField(CustomUser, related_name='rooms', blank=True)
    capacity = models.PositiveIntegerField(default=1)

    room_type = models.CharField(
            max_length=20,
            choices=(
                ('single', 'Single'),
                ('single_ensuite', 'Single Ensuite'),
                ('double', 'Double'),
                ('double_ensuite', 'Double Ensuite'),
            ),
        )
    
    
    def __str__(self):
        return f"{self.building.name} - {self.room_number}"


class RoomInspection(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    inspection_date = models.DateField(auto_now_add=True)
    inspector = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='inspections_performed')
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inspections_requested')
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('requested', 'Requested'),
            ('pending', 'Pending'),
            ('completed', 'Completed'),
        ],
        default='requested'
    )

    def __str__(self):
        return f"Inspection for {self.room} on {self.inspection_date} by {self.requested_by}"
    

class MaintenanceRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
    requested_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_requests')
    request_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')

    def __str__(self):
        return f"Maintenance Request for {self.room.room_number} on {self.request_date}"