from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

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



class RoomInspectionRequest(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='inspection_requests')
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    inspection_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    completed = models.BooleanField(default=False)

    type = models.CharField(max_length=20, choices=(
            ('check_in', 'Check-in'),
            ('check_out', 'Check-out'),
        ))

    def __str__(self):
        return f"Inspection for {self.room.room_number} requested by {self.requested_by.email}"



class RoomInspectionReport(models.Model):
    inspection_request = models.OneToOneField(RoomInspectionRequest, on_delete=models.CASCADE)
    inspector = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inspection_reports')
    report_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.inspection_request.room} by {self.inspector.email}"


class Complaint(models.Model):
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=100)
    description = models.TextField()
    CATEGORY_CHOICES = (
        ('noise', 'Noise'),
        ('maintenance', 'Maintenance'),
        ('safety', 'Safety'),
        # Add more categories as needed
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Complaint: {self.title} by {self.student.email}"
    
class MaintenanceRequest(models.Model):
    requested_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='maintenance_requests')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_requests')

    LOCATION_CHOICES = (
        ('room', 'Room'),  # Indicate maintenance request is for a specific room
        ('laundry_room', 'Laundry Room'),
        ('tv_room', 'TV Room'),
        ('stairs', 'Stairs'),
        # Add more common areas as needed
    )
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='')
    description = models.TextField()
    URGENCY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='high')
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance_requests')
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.location == 'room':
            return f"Maintenance Request: {self.description} in {self.room} by {self.student.email}"
        else:
            return f"Maintenance Request: {self.description} in {self.location} by {self.student.email}"


class RentalAgreement(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rental_agreements')
    landlord = models.CharField(max_length=100)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly')])
    start_date = models.DateField()
    end_date = models.DateField()
    agreement_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Rental Agreement for {self.student.email}"


class Bursary(models.Model):
    name = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=200, null=True, blank=True)
    reference_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    paid_by_bursary = models.BooleanField(default=False)
    is_cash_payment = models.BooleanField(default=False)
    bursary = models.ForeignKey(Bursary, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    payment_method =  ('cash paying', 'bursary')

    def __str__(self):
        return f"Payment of {self.amount} for {self.rental_agreement}"


class StudentAllocation(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='allocation')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    allocated_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.student.is_accepted = True
        self.student.save()  
        self.room.occupants.add(self.student)


    def __str__(self):
        return f"{self.student.email} - {self.room.room_number}"


@receiver(post_save, sender=StudentAllocation)
def update_room_occupants(sender, instance, **kwargs):
    instance.room.occupants.add(instance.student)



# class MaintenanceRequest(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
#     requested_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_requests')
#     request_date = models.DateField(auto_now_add=True)
#     description = models.TextField()
#     status = models.CharField(max_length=20, choices=[
#         ('pending', 'Pending'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#     ], default='pending')

#     def __str__(self):
#         return f"Maintenance Request for {self.room.room_number} on {self.request_date}"


# class Room(models.Model):
#     building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
#     room_number = models.CharField(max_length=3)
#     occupants = models.ManyToManyField(CustomUser, related_name='rooms', blank=True)
#     capacity = models.PositiveIntegerField(default=1)

#     room_type = models.CharField(
#             max_length=20,
#             choices=(
#                 ('single', 'Single'),
#                 ('single_ensuite', 'Single Ensuite'),
#                 ('double', 'Double'),
#                 ('double_ensuite', 'Double Ensuite'),
#             ),
#         )
    
    
#     def __str__(self):
#         return f"{self.building.name} - {self.room_number}"






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