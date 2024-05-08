# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student
from .forms import StudentApplicationForm, AdditionalDetailsForm
from django.contrib.auth.decorators import login_required 


def apply_view(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST)
        if form.is_valid():
            try:
                student = form.save(commit=False)
                student.application_status = 'pending'
                student.save()
                messages.success(request, 'Your application has been submitted successfully.')
                return redirect('accounts:application_confirmation')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('accounts:application_error')
    else:
        form = StudentApplicationForm()
    return render(request, 'accounts/registration.html', {'form': form})

# @login_required
# def complete_application(request, student_id, confirmation_token)
def complete_application(request, student_id):
    # try:
    #     student = Student.objects.get(confirmation_token=confirmation_token)
    # except Student.DoesNotExist:
    #     return redirect('invalid_confirmation')  # Redirect to error page

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
    

def duplicate_application(request):
    return render(request, 'accounts/application_exists.html')

def application_error(request):
    return render(request, 'accounts/application_error.html')
