from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q



# Create your models here.

CustomUser = get_user_model()  

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(help_text="Total number of students the building can accommodate")    
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
    room_number = models.CharField(max_length=3)
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
    inspector = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspections_performed')
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
        return f"Inspection for {self.room.room_number} on {self.inspection_date}"



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


# def allocate_rooms(students):
#     # Group students by gender
#     male_students = [student for student in students if student.gender == 'male']
#     female_students = [student for student in students if student.gender == 'female']

#     # Get available rooms
#     available_rooms = Room.objects.filter(
#         Q(building__gender_type='unisex') |
#         Q(building__gender_type='male', occupants__gender='male') |
#         Q(building__gender_type='female', occupants__gender='female')
#     ).annotate(
#         remaining_capacity=models.Case(
#             models.When(room_type__in=['single', 'single_ensuite'], then=models.Value(1)),
#             models.When(room_type__in=['double', 'double_ensuite'], then=models.Value(2)),
#             default=models.Value(0),
#             output_field=models.IntegerField()
#         ) - models.Count('occupants')
#     ).filter(remaining_capacity__gt=0)

#     # Allocate male students
#     for student in male_students:
#         allocate_student(student, available_rooms, 'male')

#     # Allocate female students
#     for student in female_students:
#         allocate_student(student, available_rooms, 'female')

# def allocate_student(student, available_rooms, gender):
#     # Filter available rooms based on gender
#     gender_rooms = available_rooms.filter(
#         Q(building__gender_type='unisex') |
#         Q(building__gender_type=gender)
#     )

#     # Try to allocate a room
#     for room in gender_rooms.order_by('remaining_capacity'):
#         if room.remaining_capacity >= 1:
#             room.occupants.add(student)
#             room.save()

#             # Create a RoomInspection instance with check_in=True
#             RoomInspection.objects.create(
#                 room=room,
#                 requested_by=student,
#                 check_in=True
#             )
#             break