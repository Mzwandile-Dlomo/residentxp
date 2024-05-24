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
from .models import CustomUser
from accommodations.models import LeaseAgreement, Payment
from accommodations.forms import RentalAgreementForm, PaymentMethodForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accommodations.forms import LeaseAgreementForm
from accommodations.models import LeaseAgreement


class RentalAgreementCreateView(LoginRequiredMixin, CreateView):
    model = LeaseAgreement
    form_class = RentalAgreementForm
    template_name = 'accommodations/rental_agreement.html'
    success_url = reverse_lazy('accounts:account')

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentMethodForm
    template_name = 'accommodations/payment_form.html'
    success_url = reverse_lazy('accounts:account')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = StudentForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('accounts:account')

    def get_object(self, queryset=None):
        return self.request.user

class RentalAgreementUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaseAgreement
    form_class = RentalAgreementForm
    template_name = 'accommodations/rental_agreement_update.html'
    success_url = reverse_lazy('accounts:account')
    queryset = LeaseAgreement.objects.select_related('student')

class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentMethodForm
    template_name = 'accommodations/payment_update.html'
    success_url = reverse_lazy('accounts:account')
    queryset = Payment.objects.select_related('user')



@login_required
def account_view(request):
    user = get_object_or_404(CustomUser, pk=request.user.id)
    lease_agreements = LeaseAgreement.objects.filter(student=user)
    payments = Payment.objects.filter(user=user)
    form = StudentForm(instance=user)

    print(user)
    print(lease_agreements)
    print(payments)


    context = {
        'form': form,
        'user': user,
        'lease_agreements': lease_agreements,
        'payments': payments,
        # 'edit_mode': request.GET.get('edit', False)
    }
    return render(request, 'accounts/account_page.html', context)



def lease_agreement_view(request):
  if request.method == 'POST':
    form = form = LeaseAgreementForm(request.POST, request.FILES)  

    print(form)
    if form.is_valid():
      form.save()
      messages.success(request, 'Lease agreement created successfully.')
      return redirect('accounts:account')  # Redirect to lease agreement list view
    else:
        messages.error(request, 'Please correct the errors below.')
  else:
    form = LeaseAgreementForm()
  return render(request, 'accommodations/lease_agreement.html', {'form': form})




# def account_view(request):
#     try:
#         user = get_object_or_404(CustomUser, pk=request.user.id)
#     except AttributeError:
#         messages.error(request, "Error retrieving student profile. Please contact support.")
#         return redirect('accounts:login') 

#     rental_agreements = RentalAgreement.objects.filter(student=user)
#     payments = Payment.objects.filter(user=user)
    
#     if request.method == 'POST':
#         if 'update_user' in request.POST:
#             form = StudentForm(request.POST, instance=user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Account information updated successfully!')
#                 return redirect('accounts:account')
#         elif 'sign_agreement' in request.POST:
#             agreement_id = request.POST.get('agreement_id')
#             agreement = get_object_or_404(RentalAgreement, id=agreement_id, student=user)
#             agreement_form = RentalAgreementForm(request.POST, instance=agreement)
#             if agreement_form.is_valid():
#                 agreement_form.save()
#                 messages.success(request, 'Rental agreement signed successfully!')
#                 return redirect('accounts:account')
#         elif 'update_payment' in request.POST:
#             payment_id = request.POST.get('payment_id')
#             payment = get_object_or_404(Payment, id=payment_id, user=user)
#             payment_form = PaymentMethodForm(request.POST, instance=payment)
#             if payment_form.is_valid():
#                 payment_form.save()
#                 messages.success(request, 'Payment information updated successfully!')
#                 return redirect('accounts:account')
#     else:
#         form = StudentForm(instance=user)
#         payment_forms = {payment.id: PaymentMethodForm(instance=payment) for payment in payments}
#         agreement_forms = {agreement.id: RentalAgreementForm(instance=agreement) for agreement in rental_agreements}

    
#     context = {
#         'form': form,
#         'user': user,
#         'rental_agreements': rental_agreements,
#         'payments': payments,
#         'payment_forms': payment_forms,
#         'agreement_forms': agreement_forms,
#     }
#     return render(request, 'accounts/account_page.html', context)




# def account_view(request):
#     try:
#         user = get_object_or_404(CustomUser, pk=request.user.id)
#     except AttributeError:
#         messages.error(request, "Error retrieving student profile. Please contact support.")
#         return redirect('accounts:login') 

#     rental_agreements = RentalAgreement.objects.filter(student=user)
#     payments = Payment.objects.filter(user=user)
    
#     if request.method == 'POST':
#         form = StudentForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account information updated successfully!')
#             return redirect('accounts:account')
#     else:
#         form = StudentForm(instance=user)
    
#     context = {
#         'form': form,
#         'user': user,
#         'rental_agreements': rental_agreements,
#         'payments': payments,
#         # 'edit_mode': request.GET.get('edit', False)
#     }
#     return render(request, 'accounts/account_page.html', context)


# def account_view(request):
#     try:
#         user = get_object_or_404(CustomUser, pk=request.user.id)
#     except AttributeError:
#         messages.error(request, "Error retrieving student profile. Please contact support.")
#         return redirect('accounts:login') 
    
#     if request.method == 'POST':
#         form = StudentForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account information updated successfully!')
#             return redirect('accounts:account')
#     else:
#         form = StudentForm(instance=user)

#     context = {
#         'form': form,
#         'user': request.user
#     }
#     return render(request, 'accounts/account_page.html', context)


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