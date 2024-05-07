from django.db import models
from django.core.validators import RegexValidator

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Between 9 and 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    student_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # ADDITIONAL DETAILS
    application_status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
    date_of_birth = models.DateField(null=True)
    identification = models.CharField(max_length=20, unique=True, default='Unknown', null=False)
    course = models.CharField(max_length=100, default='Unknown')
    sponsor_details = models.TextField(null=True, blank=True)
    room_type = models.CharField(max_length=50, null=True, blank=True)
    next_of_kin_full_name = models.CharField(max_length=100, null=True, blank=True)
    next_of_kin_address = models.CharField(max_length=200, null=True, blank=True)
    next_of_kin_contact = models.CharField(max_length=20, null=True, blank=True)
    next_of_kin_identification = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.full_name
