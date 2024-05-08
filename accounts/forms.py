# forms.py

from django import forms
from .models import Student
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


class StudentApplicationForm(forms.ModelForm):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    class Meta:
        model = Student
        fields = ['full_name', 'email', 'phone_number', 'student_number', 'course', 'gender', 'identification']

        # Add these lines to make fields required
        widgets = {'identification': forms.TextInput(attrs={'required': True}),
                   'student_number': forms.TextInput(attrs={'required': True})}
    def clean_identification(self):
        """Custom validation method for identification field."""
        identification = self.cleaned_data['identification']
        existing_student = Student.objects.filter(identification=identification).exists()
        if existing_student:
            # Redirect user to 'user_exists' view with an error message
            # message = 'This identification number is already in use. Please enter a unique value.'
            return redirect('accounts:duplicate_application')
        return identification

    def clean_student_number(self):
        """Custom validation method for student_number field."""
        student_number = self.cleaned_data['student_number']
        existing_student = Student.objects.filter(student_number=student_number).exists()
        if existing_student:
            # Redirect user to 'user_exists' view with an error message
            # message = 'This student number is already in use. Please enter a unique value.'
            return redirect('accounts:duplicate_application')
        return student_number
    
    def save(self, commit=True):
        student = super().save(commit=True)
        student.application_status = 'pending'
        student.save() 
        return student

class AdditionalDetailsForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['next_of_kin_full_name', 'next_of_kin_address', 'next_of_kin_identification', 'sponsor_details', 'room_type']