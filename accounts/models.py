from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, PermissionsMixin, AbstractUser, BaseUserManager, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    
class CustomUser(AbstractUser):

    username = None
    is_accepted = models.BooleanField(default=False)
    email = models.EmailField(unique=True, verbose_name='Email Address')
    
    user_type = models.CharField(max_length=20, choices=(
        ('student', 'Student'),
        ('student_leader', 'Student Leader'),
        ('admin', 'Admin'),
    ), default='student')

    # Common fields for all user types
    identification = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
    ), blank=True, null=True)

    # Student and Student Leader fields
    student_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_full_name = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_address = models.CharField(max_length=200, blank=True, null=True)
    next_of_kin_contact = models.CharField(max_length=20, blank=True, null=True)
    next_of_kin_identification = models.CharField(max_length=20, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.user_type == 'admin':
            self.room_type = None
        super().save(*args, **kwargs)

class RentalAgreement(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rental_agreements')
    landlord = models.CharField(max_length=100)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly')])
    start_date = models.DateField()
    end_date = models.DateField()
    agreement_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Rental Agreement for {self.student.email}"


class Bursary(models.Model):
    name = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=200, null=True, blank=True)
    reference_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    paid_by_bursary = models.BooleanField(default=False)
    is_cash_payment = models.BooleanField(default=False)
    bursary = models.ForeignKey(Bursary, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    payment_method =  ('cash paying', 'bursary')

    def __str__(self):
        return f"Payment of {self.amount} for {self.rental_agreement}"
