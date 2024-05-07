# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student
from .forms import StudentApplicationForm, AdditionalDetailsForm

# def apply_for_admission(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST)
#         if form.is_valid():
#             # Check if student with the same student number already exists
#             student_number = form.cleaned_data['student_number']
#             existing_student = Student.objects.filter(student_number=student_number).exists()
#             if existing_student:
#                 messages.error(request, 'Student with this student number already exists.')
#             else:
#                 student = form.save(commit=False)
#                 student.application_status = 'pending'
#                 student.save()
#                 messages.success(request, 'Your application has been submitted successfully.')
#                 return redirect('application_confirmation')
#     else:
#         form = StudentApplicationForm()
#     return render(request, 'accounts/registration.html', {'form': form})

def apply_for_admission(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST)
        if form.is_valid():
            # Check if student with the same student number already exists
            student_number = form.cleaned_data['student_number']
            existing_student = Student.objects.filter(student_number=student_number).exists()
            print("existing_student:", existing_student)
            if existing_student:
                messages.error(request, 'Student with this student number already exists. Please wait for the application process to complete.')
                return redirect('application_exists')
            else:
                student = form.save(commit=False)
                student.application_status = 'pending'
                student.save()
                messages.success(request, 'Your application has been submitted successfully.')
                return redirect('application_confirmation')
    else:
        form = StudentApplicationForm()
    return render(request, 'accounts/registration.html', {'form': form})


def complete_application(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, instance=student)
        additional_form = AdditionalDetailsForm(request.POST, instance=student)

        if form.is_valid() and additional_form.is_valid():
            form.save()
            additional_form.save()
            messages.success(request, 'Your application has been updated successfully.')
            return redirect('application_completed')
    else:
        form = StudentApplicationForm(instance=student)
        additional_form = AdditionalDetailsForm(instance=student)

    return render(request, 'accounts/complete_application.html', {'form': form, 'additional_form': additional_form})


def application_confirmation(request):
    # Retrieve user information from session
    user_id = request.session.get('user_id')

    # Check if the user has an existing pending application
    student = Student.objects.filter(application_status='pending', id=user_id).first()
    if student:
        # Pass the student_id to the complete_application view
        return redirect('accounts:complete_application', student_id=student.id)
    else:
        return render(request, 'accounts/application_confirmation.html')
    


def application_exists(request):
    return render(request, 'accounts/application_exists.html')