# forms.py

from django import forms
from .models import Student

class StudentApplicationForm(forms.ModelForm):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    class Meta:
        model = Student
        fields = ['full_name', 'email', 'phone_number', 'student_number', 'course', 'gender']

class AdditionalDetailsForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['next_of_kin_full_name', 'next_of_kin_address', 'next_of_kin_identification', 'sponsor_details', 'room_type']