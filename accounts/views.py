# from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import login, authenticate
# from .forms import UserRegistrationForm

# # Create your views here.
# def user_registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful!')
#             return redirect('home')  # Replace 'home' with the appropriate URL name
#     else:
#         form = UserRegistrationForm()

#     return render(request, 'accounts/registration.html', {'form': form})


# views.py

from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentApplicationForm

def apply_for_admission(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.application_status = 'pending'
            student.save()
            return redirect('application_confirmation')  # Redirect to confirmation page
    else:
        form = StudentApplicationForm()
    return render(request, 'accounts/registration.html', {'form': form})

def complete_application(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('application_completed')  # Redirect to completion confirmation page
    else:
        form = StudentApplicationForm(instance=student)
    return render(request, 'complete_application.html', {'form': form})
