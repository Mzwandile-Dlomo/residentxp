from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()  

# Create your models here.
class Building(models.Model):
  name = models.CharField(max_length=255)
  capacity = models.PositiveIntegerField()  # Total number of students the building can accommodate
  gender = models.CharField(max_length=10, choices=[('UN', 'Unisex'), ('M', 'Male Only'), ('F', 'Female Only')])

  def __str__(self):
    return self.name


class Room(models.Model):
  building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
  room_number = models.CharField(max_length=20)
  room_type = models.CharField(max_length=20, choices=[('S', 'Single'), ('SE', 'Single Ensuit'), ('DS', 'Double Sharing'), ('DSE', 'Double Sharing Ensuit')])  # Single, Single ensuite, Sharing, Sharing ensuite
  occupants = models.ManyToManyField(CustomUser, related_name='rooms', blank=True)
  capacity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f"{self.building.name} - {self.room_number}"


class RoomInspection(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    inspector = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who performed the inspection
    report = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')

    def __str__(self):
        return f"Inspection for {self.room} on {self.date} by {self.inspector}"


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