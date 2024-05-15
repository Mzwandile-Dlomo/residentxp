# forms.py
from django import forms
from .models import CustomUser, RentalAgreement, Bursary, Payment
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'identification', 'course', 'room')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class StudentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'identification', 'gender', 'student_number',
            'is_accepted', 'date_of_birth', 'course', 'room',
            'next_of_kin_full_name', 'next_of_kin_address',
            'next_of_kin_contact', 'next_of_kin_identification', 'bursary'
        ]







# class SignInForm(forms.ModelForm):
#     class Meta:
#         model = EndUser  # Assuming EndUser is your custom user model
#         fields = ['email', 'password']  # Fields to include in the form

#     password = forms.CharField(widget=forms.PasswordInput)  # Override password field to use PasswordInput widget


# class EndUserForm(forms.ModelForm):
#     class Meta:
#         model = EndUser
#         fields = '__all__'
#         # fields = ['first_name', 'last_name', 'email', 'phone_number', 'identification', 'gender']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # You can add any additional customization for form fields here


# class StudentForm(forms.ModelForm):
#   class Meta:
#     model = Student
#     fields = '__all__'
#     # fields = ['full_name', 'phone_number', 'identification', 'gender', 'email', 'student_number', 
#     #           'is_accepted', 'application_status', 'date_of_birth', 'course', 
#     #           'room_type', 'next_of_kin_full_name', 'next_of_kin_address', 'next_of_kin_contact', 
#     #           'next_of_kin_identification', 'bursary']


# # class StudentLeaderForm(forms.ModelForm):
# #   class Meta():
# #     model = StudentLeader
# #     fields = StudentForm.Meta.fields + ['is_student_leader']  # Add the specific field for StudentLeader

# #   def clean_is_student(self):
# #     # Validate that the user is indeed a student (is_student should be True)
# #     cleaned_data = super().clean()
# #     is_student = cleaned_data.get('is_student')
# #     if not is_student:
# #       raise ValidationError('User must be a student to be a Student Leader.')
# #     return cleaned_data
  


# class StudentUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['date_of_birth', 'course', 'room_type', 'next_of_kin_full_name', 'next_of_kin_address', 'next_of_kin_contact', 'next_of_kin_identification']

# class RentalAgreementForm(forms.ModelForm):
#     class Meta:
#         model = RentalAgreement
#         fields = '__all__'
#         # fields = ['landlord', 'rent_amount', 'payment_frequency', 'start_date', 'end_date']

     
# class BursaryForm(forms.ModelForm):
#     class Meta:
#         model = Bursary
#         fields = '__all__'
#         # fields = ['name', 'contact_information', 'reference_number']


# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = '__all__'
#         # fields = ['rental_agreement', 'amount', 'payment_date', 'paid_by_bursary']







# # class UserForm(forms.ModelForm):
# #   class Meta:
# #     model = EndUser
# #     fields = ['full_name', 'phone_number', 'identification', 'gender', 'email']


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = EndUser
#         fields = ['username', 'email', 'password']






# class StudentUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['full_name', 'email', 'phone_number', 'student_number', 'gender', 'identification']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.update({
#             'date_of_birth': forms.DateField(required=False),
#             'course': forms.CharField(max_length=100, required=False),
#             'sponsor_details': forms.CharField(widget=forms.Textarea, required=False),
#             'room_type': forms.CharField(max_length=50, required=False),
#             'next_of_kin_full_name': forms.CharField(max_length=100, required=False),
#             'next_of_kin_address': forms.CharField(max_length=200, required=False),
#             'next_of_kin_contact': forms.CharField(max_length=20, required=False),
#             'next_of_kin_identification': forms.CharField(max_length=20, required=False),
#         })



# class StudentApplicationForm(forms.ModelForm):

#     GENDER_CHOICES = (
#         ('male', 'Male'),
#         ('female', 'Female'),
#     )

#     class Meta:
#         model = CustomUser
#         fields = ['full_name', 'email', 'phone_number', 'student_number', 'gender', 'identification']

#         # Add these lines to make fields required
#         widgets = {'identification': forms.TextInput(attrs={'required': True}),
#                    'student_number': forms.TextInput(attrs={'required': True})}
#     def clean_identification(self):
#         """Custom validation method for identification field."""
#         identification = self.cleaned_data['identification']
#         existing_student = Student.objects.filter(identification=identification).exists()
#         if existing_student:
#             raise ValidationError('This identification number is already in use. Please enter a unique value.')
#         return identification

#     def clean_student_number(self):
#         """Custom validation method for student_number field."""
#         student_number = self.cleaned_data['student_number']
#         existing_student = Student.objects.filter(student_number=student_number).exists()
#         if existing_student:
#             raise ValidationError('This student number is already in use. Please enter a unique value.')
#         return student_number
    
#     def save(self, commit=True):
#         student = super().save(commit=True)
#         student.application_status = 'pending'
#         student.save() 
#         return student

# class AdditionalDetailsForm(forms.ModelForm):

#     class Meta:
#         model = Student
#         fields = ['next_of_kin_full_name', 'next_of_kin_address', 'next_of_kin_identification', 'sponsor_details', 'room_type']


# from django import forms
# from .models import Student, CustomUser

   
#     def clean_identification(self):
#         identification = self.cleaned_data['identification']
#         existing_student = Student.objects.filter(user__identification=identification).exists()
#         if existing_student:
#             raise ValidationError('This identification number is already in use. Please enter a unique value.')
#         return identification

#     def clean_student_number(self):
#         student_number = self.cleaned_data['student_number']
#         existing_student = Student.objects.filter(user__student_number=student_number).exists()
#         if existing_student:
#             raise ValidationError('This student number is already in use. Please enter a unique value.')
#         return student_number

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         student = Student.objects.create(
#             user=user,
#             date_of_birth=self.cleaned_data['date_of_birth'],
#             course=self.cleaned_data['course'],
#             sponsor_details=self.cleaned_data['sponsor_details'],
#             room_type=self.cleaned_data['room_type'],
#             next_of_kin_full_name=self.cleaned_data['next_of_kin_full_name'],
#             next_of_kin_address=self.cleaned_data['next_of_kin_address'],
#             next_of_kin_contact=self.cleaned_data['next_of_kin_contact'],
#             next_of_kin_identification=self.cleaned_data['next_of_kin_identification'],
#         )
#         if commit:
#             student.save()
#             user.save()
#         return user
    
# class StudentUpdateForm(forms.ModelForm):

#     GENDER_CHOICES = (
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('other', 'Other'),
#     )

#     phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+27 70 0000 000'. 10 digits allowed.")

#     class Meta:
#         model = CustomUser
#         model = Student
#         fields = ['full_name', 'email', 'phone_number', 'course', 'gender', 'identification',
#                   'next_of_kin_full_name', 'next_of_kin_address', 'next_of_kin_identification', 'sponsor_details', 'room_type']

#         # Make all fields optional using widgets with empty attributes
#         widgets = {
#             'full_name': forms.TextInput(attrs={'disabled': True}),
#             'email': forms.EmailInput(attrs={}),
#             'phone_number': forms.TextInput(attrs={}),
#             'student_number': forms.TextInput(attrs={'disabled': True}),
#             'course': forms.TextInput(attrs={}),
#             'gender': forms.Select(attrs={'disabled': True}),
#             'identification': forms.TextInput(attrs={}),
#             'next_of_kin_full_name': forms.TextInput(attrs={}),
#             'next_of_kin_address': forms.TextInput(attrs={}),
#             'next_of_kin_identification': forms.TextInput(attrs={}),
#             'sponsor_details': forms.Textarea(attrs={}),
#             'room_type': forms.TextInput(attrs={}),
#         }

#     def clean_identification(self):
#         """Custom validation method for identification field."""
#         identification = self.cleaned_data['identification']
#         existing_student = Student.objects.filter(identification=identification).exists()
#         if existing_student:
#             raise ValidationError('This identification number is already in use. Please enter a unique value.')
#         return identification

#     def clean_student_number(self):
#         """Custom validation method for student_number field."""
#         student_number = self.cleaned_data['student_number']
#         existing_student = Student.objects.filter(student_number=student_number).exists()
#         if existing_student:
#             raise ValidationError('This student number is already in use. Please enter a unique value.')
#         return student_number

#     def save(self, commit=True):
#         student = super().save(commit=False)  # Prevent initial save, set application status later
        

#         for field in self.changed_data:
#             setattr(student, field, self.cleaned_data[field])

#         # Set application status (optional)
#         # student.application_status = 'pending'

#         if commit:
#             student.save()
#         return student