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
from datetime import date

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
        'form': form,
        'user': request.user
    }
    return render(request, 'accounts/account_page.html', context)

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('core:home')
        else:
            context = {'form': form}
            return render(request, 'accounts/registration_page.html', context)
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/registration_page.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
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

def update_view(request):
    user = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'POST':
        print(request.POST)
        form = StudentForm(request.POST, instance=user)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account information updated successfully!')
            return redirect('accounts:account')
    else:
        form = StudentForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'accounts/account_update_page.html', context)


def logout_view(request):
    logout(request)
    # Redirect to the home page or any other desired page
    return redirect('core:home')


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