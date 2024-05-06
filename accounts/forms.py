# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('This email address is already registered.')
#         return email


# forms.py

from django import forms
from .models import Student

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'phone_number', 'student_number', 'gender']
