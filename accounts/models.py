from django.db import models

# Create your models here.
# models.py

class Student(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    student_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    application_status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')

    # Additional fields to be completed upon acceptance
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True)
    course_of_interest = models.CharField(max_length=100, blank=True)
    academic_achievements = models.TextField(blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.full_name
