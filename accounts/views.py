# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.db import IntegrityError
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, StudentForm


def account_view(request):
    try:
        user = get_object_or_404(CustomUser, pk=request.user.id)
    except AttributeError:
        messages.error(request, "Error retrieving student profile. Please contact support.")
        return redirect('accounts:login') 
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account information updated successfully!')
            return redirect('accounts:account')
    else:
        form = StudentForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'accounts/account_page.html', context)

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't commit yet for password hashing
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Handle successful registration (e.g., redirect, confirmation message)
            redirect('core:home')
        else:
            context = {'form': form}from django.shortcuts import render, redirect, get_object_or_404

            return render(request, 'accounts/registration_page.html', context)
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/registration_page.html', context)  # Adjust template name


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('core:home')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    # Redirect to the home page or any other desired page
    return redirect('core:home')



@login_required
def profile_view(request):
    if request.user.is_authenticated:
        try:
            user = get_object_or_404(CustomUser, pk=request.user.id)
        except AttributeError:
            messages.error(request, "Error retrieving student profile. Please contact support.")
            return redirect('accounts:login')  # Or redirect to appropriate page

        # ... handle existing student profile logic ...
            # Handle potential form submissions
        if request.method == 'POST':
            # Handle Student Update Form
            student_form = StudentUpdateForm(request.POST, instance=student)
            if student_form.is_valid():
                student_form.save()
                messages.success(request, 'Profile updated successfully!')

            # Handle RentalAgreement Form
            rental_agreement_form = RentalAgreementForm(request.POST)
            if rental_agreement_form.is_valid():
                rental_agreement = rental_agreement_form.save(commit=False)
                rental_agreement.student = user
                rental_agreement.save()
                messages.success(request, 'Rental agreement signed successfully!')

            # Handle Bursary Form
            bursary_form = BursaryForm(request.POST)
            if bursary_form.is_valid():
                bursary = bursary_form.save()
                user.bursary = bursary
                user.save()
                messages.success(request, 'Bursary information updated successfully!')

            return redirect('accounts:profile')

        # Prefill forms with existing data
        student_form = StudentUpdateForm(instance=student)
        rental_agreement_form = RentalAgreementForm(instance=student.rental_agreements.first()) if student.rental_agreements.exists() else RentalAgreementForm()
        bursary_form = BursaryForm(instance=student.bursary) if student.bursary else BursaryForm()

        context = {
            'user': request.user,
            'student_form': student_form,
            'rental_agreement_form': rental_agreement_form,
            'bursary_form': bursary_form,
            'edit_url': reverse('accounts:update'),
            'student': student,
        }
        return render(request, 'accounts/account_page.html', context)
    

def rental_agreement(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)

    if request.method == 'POST':
        form = RentalAgreementForm(request.POST)
        if form.is_valid():
            rental_agreement = form.save(commit=False)
            rental_agreement.student = student
            rental_agreement.save()
            return redirect('rental_agreement_detail', rental_agreement_id=rental_agreement.id)
    else:
        form = RentalAgreementForm()

    return render(request, 'rental_agreement.html', {'form': form, 'student': student})

# #     else:
# #         # User is not authenticated, handle accordingly
# #         messages.info(request, "You need to be logged in to access your profile.")
# #         return redirect('accounts:login')


# @login_required
# def profile_view(request):
#     try:
#         user = EndUser.objects.get(id=request.user.id)
#         student = Student.objects.get(user_ptr=user)
#     except Student.DoesNotExist:
#         messages.info(request, "You don't have a linked student record yet. Apply to become a student!")
#         return redirect('accounts:signup')

#     # Handle potential form submissions
#     if request.method == 'POST':
#         # Handle Student Update Form
#         student_form = StudentUpdateForm(request.POST, instance=student)
#         if student_form.is_valid():
#             student_form.save()
#             messages.success(request, 'Profile updated successfully!')

#         # Handle RentalAgreement Form
#         rental_agreement_form = RentalAgreementForm(request.POST)
#         if rental_agreement_form.is_valid():
#             rental_agreement = rental_agreement_form.save(commit=False)
#             rental_agreement.student = student
#             rental_agreement.save()
#             messages.success(request, 'Rental agreement signed successfully!')

#         # Handle Bursary Form
#         bursary_form = BursaryForm(request.POST)
#         if bursary_form.is_valid():
#             bursary = bursary_form.save()
#             student.bursary = bursary
#             student.save()
#             messages.success(request, 'Bursary information updated successfully!')

#         return redirect('accounts:profile')

#     # Prefill forms with existing data
#     student_form = StudentUpdateForm(instance=student)
#     rental_agreement_form = RentalAgreementForm(instance=student.rental_agreements.first()) if student.rental_agreements.exists() else RentalAgreementForm()
#     bursary_form = BursaryForm(instance=student.bursary) if student.bursary else BursaryForm()

#     context = {
#         'user': request.user,
#         'student_form': student_form,
#         'rental_agreement_form': rental_agreement_form,
#         'bursary_form': bursary_form,
#         'edit_url': reverse('accounts:update'),
#         'student': student,
#     }

#     return render(request, 'accounts/account_page.html', context)


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Basic form validation
#         if not email or not password:
#             messages.error(request, 'Email and password are required.')
#             return render(request, 'accounts/login.html')
        
#         # Authenticate user
#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('accounts:profile')
#         else:
#             messages.error(request, 'Invalid email or password.')
#             return render(request, 'accounts/login.html')


# def logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
#     return redirect('accounts:login')



# def signup_view(request):
#     if request.method == 'POST':
#         form = EndUserForm(request.POST)
#         if form.is_valid():
#             end_user = form.save()
#             student = Student.objects.create(user=end_user)
#             student.save()

#             user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
#             if user is not None:
#                 login(request, user)
                
#                 # Redirect to the user's profile page
#                 return redirect('accounts:profile')


#     else:
#         form = EndUserForm()
#     return render(request, 'accounts/signup.html', {'form': form})

# def signin_view(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')  # Redirect to the profile page after successful login
#             else:
#                 # Authentication failed, show error message
#                 form.add_error(None, "Invalid email or password")
#     else:
#         form = SignInForm()
#     return render(request, 'accounts/signin.html', {'form': form})


# def registration_view(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():

#             email = form.cleaned_data['email']
#             identification = form.cleaned_data['identification']

#             if EndUser.objects.filter(email=email).exists() or EndUser.objects.filter(identification=identification).exists():
#                 # Handle the case where the email or identification is already in use
#                 return render(request, 'registration.html', {'form': form, 'error_message': 'Email or identification already in use.'})
#             try:
#                 # Create User instance
#                 user = form.save()
#                 # Create Student instance with the created user
#                 student = Student.objects.create(
#                     full_name=user.full_name,
#                     phone_number=user.phone_number,
#                     identification=user.identification,
#                     gender=user.gender,
#                     email=user.email,
#                     # Add other fields specific to Student model here
#                 )
#                 # Save the Student instance
#                 student.save()

#                 # subject = 'Your Application Confirmation'
#                 # message = f'Dear {user.full_name},\n\nThank you for your application to become a student. We have received your information and it is currently under review.\n\nYou will receive a follow-up email with further instructions shortly.\n\nBest regards,\nThe Admissions Team'
#                 # from_email = settings.EMAIL_HOST_USER
#                 # to = user.email
#                 # send_mail(subject, message, from_email, [to], fail_silently=False)

#                 # subject = 'Follow-Up on Your Application'
#                 # message = f'Dear {user.full_name},\n\nThank you for your application. Please use the following unique ID to provide additional details: {unique_token}\n\nClick here to provide additional details: {settings.BASE_URL}/additional-details/{unique_token}\n\nBest regards,\nThe Admissions Team'
#                 # send_mail(subject, message, from_email, [to], fail_silently=False)

#                 messages.success(request, 'Your application has been submitted successfully.')
#                 return redirect('accounts:profile')
#             except IntegrityError as e:
#                 # Handle IntegrityError, if any
#                 return redirect(request, 'accounts/registration.html', {'form': form, 'error_message': str(e)})
#         else:
#             return render(request, 'accounts/registration.html', {'form': form, 'error_message': "User exists"})
#     else:
#         form = UserForm()
#     return render(request, 'accounts/registration.html', {'form': form})


# @login_required
# def updateProfile_view(request):
#     student = get_object_or_404(Student, email=request.user.email)
#     if request.method == 'POST':
#         form = StudentUpdateForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             student.application_status = 'pending'
#             student.save()
#             return redirect('profile')
#     else:
#         form = StudentUpdateForm(instance=student)
#     return render(request, 'update_profile.html', {'form': form})


# def duplicate_application_view(request):
#     return render(request, 'accounts/application_exists.html')

# def application_error_view(request):
#     return render(request, 'accounts/application_error.html')







# def application_confirmation_view(request):
#     # Retrieve user information from session
#     user_id = request.session.get('user_id')

#     # Check if the user has an existing pending application
#     student = Student.objects.filter(application_status='pending', id=user_id).first()
#     if student:
#         # Pass the student_id to the complete_application view
#         return redirect('accounts:complete_application', student_id=student.id)
#     else:
#         return render(request, 'accounts/application_confirmation.html')



# def additionalDetails_view(request):
#     student = get_object_or_404(Student, email=request.user.email)
#     if student.is_accepted:  # Check if the student is accepted
#         if request.method == 'POST':
#             form = AdditionalDetailsForm(request.POST, instance=student)
#             if form.is_valid():
#                 form.save()
#                 student.application_status = 'completed'
#                 student.save()
#                 return redirect('main_view')  # Redirect to the main view
#         else:
#             form = AdditionalDetailsForm(instance=student)
#         return render(request, 'additional_details.html', {'form': form})
#     else:
#         messages.info(request, "Your application is still pending review. You will receive an email once it is accepted.")
#         return redirect('accounts:profile')
    
























# @login_required
# def profile_view(request):

#     try:
#         user = User.objects.get(id=request.user.id)
#         student = Student.objects.get(user_ptr=user)

#     except Student.DoesNotExist:
#         messages.info(request, "You don't have a linked student record yet. Apply to become a student!")
#         return redirect('accounts:signup')

#     # Handle potential form submission for profile updates (optional)
#     if request.method == 'POST':
#         form = StudentUpdateForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('accounts:profile')  # Redirect back to account page

#     form = StudentUpdateForm(instance=student)  # Pre-populate with student data

#     context = {'user': request.user, 'form': form, 'edit_url': reverse('accounts:update'), 'student': student}

#     return render(request, 'accounts/account_page.html', context)




# def signup_view(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Get the form data
#                 email = form.cleaned_data['email']
#                 password = form.cleaned_data['student_number']  # Use student number as password
#                 full_name = form.cleaned_data['full_name']
#                 phone_number = form.cleaned_data['phone_number']
#                 student_number = form.cleaned_data['student_number']
#                 gender = form.cleaned_data['gender']
#                 identification = form.cleaned_data['identification']

#                 # Create a new CustomUser instance
#                 user = CustomUser.objects.create_user(email=email, password=password)

#                 # Create a new Student instance and associate it with the CustomUser
#                 student = Student.objects.create(
#                     user=user,
#                     full_name=full_name,
#                     phone_number=phone_number,
#                     student_number=student_number,
#                     gender=gender,
#                     identification=identification,
#                     application_status='pending',
#                     is_accepted=False,
#                 )

                
#                 # Generate a unique token for additional details
#                 student.unique_token = get_random_string(length=32)
#                 student.save()

#                 # Send application confirmation email
#                 subject = 'Your Application Confirmation'
#                 message = f'Dear {student.full_name},\n\nThank you for your application to become a student. We have received your information and it is currently under review.\n\nYou will receive a follow-up email with further instructions shortly.\n\nBest regards,\nThe Admissions Team'
#                 from_email = settings.EMAIL_HOST_USER  # Use configured email from settings
#                 to = student.email
#                 send_mail(subject, message, from_email, [to], fail_silently=False)  # Handle sending errors

#                 # Send follow-up email with unique token (consider using a dedicated email library for HTML content)
#                 subject = 'Follow-Up on Your Application'
#                 message = f'Dear {student.full_name},\n\nThank you for your application. Please use the following unique ID to provide additional details: {student.unique_token}\n\nClick here to provide additional details: {settings.BASE_URL}/additional-details/{student.unique_token}\n\nBest regards,\nThe Admissions Team'
#                 send_mail(subject, message, from_email, [to], fail_silently=False)  # Handle sending errors


#                 messages.success(request, 'Your application has been submitted successfully.')
#                 return redirect('accounts:application_confirmation')

#             except Exception as e:
#                 messages.error(request, f"An error occurred: {e}")
#                 return redirect('accounts:application_error')
#         else:
#             messages.error(request, 'Please correct the errors in the application form.')
#     else:
#         form = StudentApplicationForm()

#     return render(request, 'accounts/registration.html', {'form': form})



# def signup_view(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Create a new user instance
#                 email = form.cleaned_data['email']
#                 student_number = form.cleaned_data['student_number']
#                 password = get_random_string(length=12)  # Generate a random password for the user
#                 user = User.objects.create_user(username=student_number, email=email, password=password)

#                 # Create the student instance and associate it with the user
#                 student = form.save(commit=False)
#                 student.user = user
#                 student.application_status = 'pending'
#                 student.is_accepted = False
#                 student.save()

#                 # Generate a unique token for additional details
#                 student.unique_token = get_random_string(length=32)
#                 student.save()

#                 # Send application confirmation email
#                 subject = 'Your Application Confirmation'
#                 message = f'Dear {student.full_name},\n\nThank you for your application to become a student. We have received your information and it is currently under review.\n\nYou will receive a follow-up email with further instructions shortly.\n\nBest regards,\nThe Admissions Team'
#                 from_email = settings.EMAIL_HOST_USER  # Use configured email from settings
#                 to = student.email
#                 send_mail(subject, message, from_email, [to], fail_silently=False)  # Handle sending errors

#                 # Send follow-up email with unique token (consider using a dedicated email library for HTML content)
#                 subject = 'Follow-Up on Your Application'
#                 message = f'Dear {student.full_name},\n\nThank you for your application. Please use the following unique ID to provide additional details: {student.unique_token}\n\nClick here to provide additional details: {settings.BASE_URL}/additional-details/{student.unique_token}\n\nBest regards,\nThe Admissions Team'
#                 send_mail(subject, message, from_email, [to], fail_silently=False)  # Handle sending errors

#                 messages.success(request, 'Your application has been submitted successfully. Please check your email for further instructions.')

#                 return redirect('accounts:application_confirmation')

#             except Exception as e:
#                 messages.error(request, f"An error occurred: {e}")
#                 return HttpResponse(e)
#                 # return redirect('accounts:application_error')
#         else:
#             messages.error(request, 'Please correct the errors in the application form.')
#     else:
#         form = StudentApplicationForm()

#     return render(request, 'accounts/registration.html', {'form': form})

# def signup_view(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST)
#         if form.is_valid():
#             try:
#                 student = form.save(commit=False)
#                 student.application_status = 'pending'
#                 student.user = request.user
#                 student.is_accepted = False
#                 student.save()

#                 # Generate a unique token for additional details
#                 student.unique_token = get_random_string(length=32)
#                 student.save()

#                 # Send application confirmation email
#                 subject = 'Your Application Confirmation'
#                 message = f'Dear {student.full_name},\n\nThank you for your application to become a student. We have received your information and it is currently under review.\n\nYou will receive a follow-up email with further instructions shortly.\n\nBest regards,\nThe Admissions Team'
#                 from_email = settings.EMAIL_HOST_USER  # Use configured email from settings
#                 to = student.email
#                 send_mail(subject, message, from_email, [to], fail_silently=False)  # Handle sending errors

#                 # Send follow-up email with unique token (consider using a dedicated email library for HTML content)
#                 subject = 'Follow-Up on Your Application'
#                 message = f'Dear {student.full_name},\n\nThank you for your application. Please use the following unique ID to provide additional details: {student.unique_token}\n\nClick here to provide additional details: {settings.BASE_URL}/additional-details/{student.unique_token}\n\nBest regards,\nThe Admissions Team'
#                 send_mail(subject, message, from_email, [to], fail_silently=False)  # Handle sending errors

#                 messages.success(request, 'Your application has been submitted successfully. Please check your email for further instructions.')

#                 return redirect('accounts:application_confirmation')

#             except Exception as e:
#                 messages.error(request, f"An error occurred: {e}")
#                 return HttpResponse(e)
#                 # return redirect('accounts:application_error')
#         else:
#             messages.error(request, 'Please correct the errors in the application form.')

#     else:
#         form = StudentApplicationForm()

#     return render(request, 'accounts/registration.html', {'form': form})
