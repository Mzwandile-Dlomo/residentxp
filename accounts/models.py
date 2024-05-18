from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

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
