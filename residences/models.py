# residences/models.py
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser

class Building(models.Model):
    BUILDING_GENDER_CHOICES = (
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('mixed', 'Mixed'),
    )
    
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=BUILDING_GENDER_CHOICES)

    def __str__(self):
        return self.name

    @property
    def num_of_occupants(self):
        return sum(room.occupants.count() for room in self.rooms.all())

    @property
    def occupants_by_type(self):
        occupants = CustomUser.objects.filter(rooms__building=self).distinct()
        occupants_type_count = {
            user_type: occupants.filter(user_type=user_type).count()
            for user_type, _ in CustomUser.USER_TYPE_CHOICES
        }
        return occupants_type_count

class RoomItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'Single Room'),
        ('single_ensuite', 'Single Ensuite'),
        ('sharing', 'Sharing Room'),
        ('sharing_ensuite', 'Sharing Ensuite'),
    )

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='sharing')
    capacity = models.PositiveIntegerField(default=2)
    occupants = models.ManyToManyField(CustomUser, related_name='rooms', blank=True)
    items = models.ManyToManyField(RoomItem, related_name='rooms')

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"

    @property
    def is_full(self):
        return self.occupants.count() >= self.capacity

    @property
    def vacancies(self):
        return self.capacity - self.occupants.count()

    def clean(self):
        # Ensure occupants' gender matches building's gender restriction
        if self.building.gender in ['boys', 'girls']:
            for occupant in self.occupants.all():
                if self.building.gender == 'boys' and occupant.gender != 'male':
                    raise ValidationError("This building is for boys only.")
                if self.building.gender == 'girls' and occupant.gender != 'female':
                    raise ValidationError("This building is for girls only.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class RoomInspection(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='inspections')
    inspected_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='room_inspections', limit_choices_to={'user_type': 'student_leader'})
    inspection_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    items_present = models.ManyToManyField(RoomItem, related_name='room_inspections')

    def __str__(self):
        return f"Inspection of {self.room} on {self.inspection_date}"
