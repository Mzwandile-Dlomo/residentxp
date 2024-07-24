from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date


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

    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=3800.00)

    
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

    ensuite_additional_rent = models.DecimalField(max_digits=10, decimal_places=2, default=800.0)

    
    
    def __str__(self):
        return f"{self.building.name} - {self.room_number}"

    def has_available_beds(self):
        return self.capacity > self.occupants.count()

    def get_rent_amount(self):
        base_rent = self.building.rent_amount
        if self.room_type.endswith('ensuite'):
            return base_rent + self.ensuite_additional_rent
        return base_rent
    


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



class LeaseAgreement(models.Model):
    SEMESTER_CHOICES = [
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
        ('both', 'Both Semesters'),
    ]

    PAYMENT_FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly')
    ]
    
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lease_agreements')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='lease_agreements', null=True)
    landlord = models.CharField(max_length=100)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='both')
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES, default='monthly')
    start_date = models.DateField()
    end_date = models.DateField()
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    agreement_signed = models.BooleanField(default=False)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lease_terms = models.TextField(null=True, blank=True)  # Add any specific lease terms and conditions here

    def __str__(self):
        return f"Lease Agreement for {self.student.email}"

    def save(self, *args, **kwargs):
        if not self.agreement_signed:
            raise ValidationError("Lease agreement must be signed before saving.")
        if not self.start_date or not self.end_date:
            current_year = date.today().year
            if self.semester == 'first':
                self.start_date = date(current_year, 1, 1)
                self.end_date = date(current_year, 5, 31)
            elif self.semester == 'second':
                self.start_date = date(current_year, 8, 1)
                self.end_date = date(current_year, 12, 31)
            elif self.semester == 'both':
                self.start_date = date(current_year, 1, 1)
                self.end_date = date(current_year, 12, 31)
        super().save(*args, **kwargs)
        # Approve the room reservation associated with this lease agreement
        room_reservation = RoomReservation.objects.filter(student=self.student, room=self.room).first()
        if room_reservation:
            room_reservation.status = 'approved'
            room_reservation.save()


class Bursary(models.Model):
    name = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=200, null=True, blank=True)
    reference_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    lease_agreement = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE, related_name='payments', default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    paid_by_bursary = models.BooleanField(default=False)
    is_cash_payment = models.BooleanField(default=False)
    bursary = models.ForeignKey(Bursary, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')

    # Cash Payment Details
    cash_payment_reference = models.CharField(max_length=100, null=True, blank=True)
    cash_payment_date = models.DateField(null=True, blank=True)
    cash_payment_method = models.CharField(max_length=50, null=True, blank=True)

    # Bursary Payment Details
    bursary_name = models.CharField(max_length=100, null=True, blank=True)
    bursary_reference_number = models.CharField(max_length=50, null=True, blank=True)
    bursary_payment_date = models.DateField(null=True, blank=True)
    bursary_contact_information = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.lease_agreement}"

    def save(self, *args, **kwargs):
        # Ensure the appropriate fields are filled based on the payment type
        if self.is_cash_payment:
            if not self.cash_payment_reference:
                raise ValueError("Cash payment reference must be provided for cash payments.")
        if self.paid_by_bursary:
            if not self.bursary or not self.bursary_reference_number:
                raise ValueError("Bursary and bursary reference number must be provided for bursary payments.")
        super().save(*args, **kwargs)



class RoomReservation(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')

    def __str__(self):
        return f"{self.student.first_name} - {self.room.room_number} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.room.room_type.endswith('ensuite'):
            raise ValueError("Only ensuite rooms can be reserved.")
        
        super().save(*args, **kwargs)


class StudentAllocation(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='allocation')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    allocated_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.room.has_available_beds():
            raise ValueError("Room is already full")
        
        # Check for existing reservations for this room
        existing_reservations = RoomReservation.objects.filter(
            room=self.room, status__in=['pending', 'approved']
        )

        if existing_reservations.exists():
            # Reject allocation if there are pending or approved reservations
            reservations = ", ".join([str(r) for r in existing_reservations])
            raise ValueError(f"Room reservation(s) {reservations} exist for this room")   

        super().save(*args, **kwargs)
        self.student.is_accepted = True
        self.student.save()  
        self.room.occupants.add(self.student)


    def __str__(self):
        return f"{self.student.email} - {self.room.room_number}"








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