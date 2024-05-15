from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()  # Replace with your custom user model if applicable

# Create your models here.
class Building(models.Model):
  name = models.CharField(max_length=255)
  capacity = models.PositiveIntegerField()  # Total number of students the building can accommodate
  gender = models.CharField(max_length=10, choices=[('UN', 'Unisex'), ('M', 'Male Only'), ('F', 'Female Only')])

  def __str__(self):
    return self.name

class RoomType(models.Model):
  name = models.CharField(max_length=20, choices=[('S', 'Single'), ('SE', 'Single Ensuit'), ('DS', 'Double Sharing'), ('DSE', 'Double Sharing Ensuit')])  # Single, Single ensuite, Sharing, Sharing ensuite

class Room(models.Model):
  building = models.ForeignKey(Building, on_delete=models.CASCADE)
  room_number = models.CharField(max_length=20)
  room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
  occupants = models.ManyToManyField(CustomUser, related_name='rooms', blank=True)
  capacity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f"{self.building.name} - {self.room_number}"


class RoomInspection(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    inspector = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who performed the inspection
    report = models.TextField()

    def __str__(self):
        return f"Inspection for {self.room} on {self.date} by {self.inspector}"
