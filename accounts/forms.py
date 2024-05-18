# forms.py
from django import forms
from .models import CustomUser
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'identification', 'course')

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
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name' ,'email', 'identification', 'gender', 
            'student_number', 'date_of_birth', 'course', 'next_of_kin_full_name', 
            'next_of_kin_address', 'next_of_kin_contact', 'next_of_kin_identification',
        ]
        required = (
            'first_name', 'last_name', 'email', 'identification', 'gender',
            'student_number', 'date_of_birth', 'course', 'next_of_kin_full_name',
            'next_of_kin_address', 'next_of_kin_contact', 'next_of_kin_identification',
        )
        
        def clean_date_of_birth(self):
            date_of_birth = self.cleaned_data.get('date_of_birth')
            if not date_of_birth:
                raise ValidationError('Date of birth is required.')
            return date_of_birth
