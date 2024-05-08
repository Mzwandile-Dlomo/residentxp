from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.core.exceptions import ValidationError



class Student(models.Model):
    #Step 1
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
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+27 70 0000 000'. 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    student_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    identification = models.CharField(max_length=20, unique=True, null=False)


    #Step 2
    # ADDITIONAL DETAILS
    # confirmation_token = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    application_status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
    date_of_birth = models.DateField(null=True)
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
    
    def clean_identification(self):
        """Custom validation method for identification field."""
        existing_student = Student.objects.filter(identification=self.cleaned_data['identification']).exists()
        if existing_student:
            raise ValidationError('This identification number is already in use. Please enter a unique value.')
        return self.cleaned_data['identification']
    
    def clean_student_number(self):
        """Custom validation method for student_number field."""
        existing_student = Student.objects.filter(student_number=self.cleaned_data['student_number']).exists()
        if existing_student:
            raise ValidationError('This student number is already in use. Please enter a unique value.')
        return self.cleaned_data['student_number']

