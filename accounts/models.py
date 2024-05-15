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
    ROOM_TYPE_CHOICES = (
        ('single', 'Single Room'),
        ('single_ensuite', 'Single Ensuite'),
        ('sharing', 'Sharing Room'),
        ('sharing_ensuite', 'Sharing Ensuite'),
    )

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
        ('other', 'Other'),
    ), blank=True, null=True)

    # Student and Student Leader fields
    student_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_full_name = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_address = models.CharField(max_length=200, blank=True, null=True)
    next_of_kin_contact = models.CharField(max_length=20, blank=True, null=True)
    next_of_kin_identification = models.CharField(max_length=20, blank=True, null=True)
    bursary = models.ForeignKey('Bursary', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

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

class Payment(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    paid_by_bursary = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount} for {self.rental_agreement}"

class Bursary(models.Model):
    name = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=200, null=True, blank=True)
    reference_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name








# class UserManager(BaseUserManager):
#     def create_user(self, email, full_name, phone_number, identification, gender, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, full_name=full_name, phone_number=phone_number, identification=identification, gender=gender, **extra_fields)
#         if password:
#             user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, full_name, phone_number, identification, gender, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(email, full_name, phone_number, identification, gender, password, **extra_fields)


# class EndUser(AbstractUser):
#     username = None
#     email = models.EmailField(max_length=100, unique=True)
#     phone_number = models.CharField(max_length=20)
#     identification = models.CharField(max_length=15, unique=True)
#     gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))


#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_name='enduser_set',
#         related_query_name='enduser',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name='enduser_set',
#         related_query_name='enduser',
#     )
    
#     def __str__(self):
#         return self.first_name

#     def get_full_name(self):
#         return self.first_name + self.last_name

#     def get_short_name(self):
#         return self.first_name

        # return f"Payment of {self.amount} for {self.rental_agreement.student.user.username}"


# EndUser._meta.get_field("groups").related_name = "enduser_groups"
# EndUser._meta.get_field("user_permissions").related_name = "enduser_user_permissions"



# class Student(models.Model):
#     is_student = models.BooleanField(default=True)

#     user = models.OneToOneField(EndUser, on_delete=models.CASCADE, related_name='student_profile')
#     student_number = models.CharField(max_length=20, unique=True, blank=True)
#     is_accepted = models.BooleanField(default=False)
#     application_status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
#     date_of_birth = models.DateField(blank=True, null=True)
#     course = models.CharField(max_length=100, blank=True, null=True)
#     bursary = models.ForeignKey(Bursary, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     room_type = models.CharField(max_length=50, null=True, blank=True)
#     next_of_kin_full_name = models.CharField(max_length=100, null=True, blank=True)
#     next_of_kin_address = models.CharField(max_length=200, null=True, blank=True)
#     next_of_kin_contact = models.CharField(max_length=20, null=True, blank=True)
#     next_of_kin_identification = models.CharField(max_length=20, null=True, blank=True)


# class StudentLeader(Student):
#     is_student_leader = models.BooleanField(default=True)
#     # Add specific fields for Student Leaders here (e.g., leadership position)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} (Student Leader)"




# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.utils import timezone
# from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.contrib.auth.models import AbstractUser, Group
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils import timezone
# from django.contrib.auth.models import Permission


# class UserManager(BaseUserManager):
#     def create_user(self, email, full_name, phone_number, identification, gender, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, full_name=full_name, phone_number=phone_number, identification=identification, gender=gender, **extra_fields)
#         if password:
#             user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, full_name, phone_number, identification, gender, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(email, full_name, phone_number, identification, gender, password, **extra_fields)

# class User(AbstractBaseUser):
#     full_name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=20)  # Changed max_length to 20
#     identification = models.CharField(max_length=15, unique=True)
#     gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name', 'phone_number', 'identification', 'gender']

#     def __str__(self):
#         return self.full_name

#     def get_full_name(self):
#         return self.full_name

#     def get_short_name(self):
#         return self.full_name
    

# class Student(User):
#     is_student = models.BooleanField(default=True)

#     student_number = models.CharField(max_length=20, unique=True, blank=True)
#     is_accepted = models.BooleanField(default=False)
#     application_status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
#     date_of_birth = models.DateField(blank=True, null=True)
#     course = models.CharField(max_length=100, blank=True, null=True)
#     sponsor_details = models.TextField(null=True, blank=True)
#     room_type = models.CharField(max_length=50, null=True, blank=True)
#     next_of_kin_full_name = models.CharField(max_length=100, null=True, blank=True)
#     next_of_kin_address = models.CharField(max_length=200, null=True, blank=True)
#     next_of_kin_contact = models.CharField(max_length=20, null=True, blank=True)
#     next_of_kin_identification = models.CharField(max_length=20, null=True, blank=True)

# class StudentLeader(Student):
#     is_student_leader = models.BooleanField(default=True)
#     # Add specific fields for Student Leaders here (e.g., leadership position)

#     def __str__(self):
#         return f"{self.full_name} (Student Leader)"

# class Admin(User, PermissionsMixin):
#     # Add specific fields for Admins here (e.g., department, permissions)
#     groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='admin_groups')
#     user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='admin_permissions')

#     def __str__(self):
#         return f"{self.full_name} (Admin)"


# class Bursary(models.Model):
#     name = models.CharField(max_length=100)
#     contact_information = models.CharField(max_length=200, null=True, blank=True)
#     reference_number = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class RentalAgreement(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     landlord = models.CharField(max_length=100)
#     rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly')])
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"Rental Agreement for {self.student.user.username}"

# class Payment(models.Model):
#     rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateField()
#     paid_by_bursary = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Payment of {self.amount} for {self.rental_agreement.student.user.username}"

# # class CustomUser(AbstractUser):
# #     GENDER_CHOICES = [
# #         ('male', 'Male'),
# #         ('female', 'Female'),
# #         ('other', 'Other'),
# #     ]

# #     is_student = models.BooleanField(default=False)
# #     is_student_leader = models.BooleanField(default=False)

# #     full_name = models.CharField(max_length=100)
# #     email = models.EmailField(unique=True)
# #     phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+27 70 0000 000'. 10 digits allowed.")
# #     phone_number = models.CharField(validators=[phone_regex], max_length=15)
# #     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
# #     identification = models.CharField(max_length=20, unique=True, null=True, blank=True)

# #     # Add related_name arguments to avoid conflicts
# #     groups = models.ManyToManyField(
# #         'auth.Group',
# #         related_name='customuser_set',  # Changed related_name here
# #         blank=True,
# #         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
# #         verbose_name='groups'
# #     )
# #     user_permissions = models.ManyToManyField(
# #         'auth.Permission',
# #         related_name='customuser_set',  # Changed related_name here
# #         blank=True,
# #         help_text='Specific permissions for this user.',
# #         verbose_name='user permissions'
# #     )

# # class Student(models.Model):
# #     APPLICATION_STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('accepted', 'Accepted'),
# #         ('rejected', 'Rejected'),
# #     ]


# #     is_student = models.BooleanField(default=True)

# #     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student')
# #     student_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

# #     # ADDITIONAL DETAILS
# #     is_accepted = models.BooleanField(default=False)
# #     application_status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
# #     date_of_birth = models.DateField(blank=True, null=True)
# #     course = models.CharField(max_length=100, blank=True, null=True)
# #     sponsor_details = models.TextField(null=True, blank=True)
# #     room_type = models.CharField(max_length=50, null=True, blank=True)
# #     next_of_kin_full_name = models.CharField(max_length=100, null=True, blank=True)
# #     next_of_kin_address = models.CharField(max_length=200, null=True, blank=True)
# #     next_of_kin_contact = models.CharField(max_length=20, null=True, blank=True)
# #     next_of_kin_identification = models.CharField(max_length=20, null=True, blank=True)

# #     def clean_identification(self):
# #         """Custom validation method for identification field."""
# #         existing_student = Student.objects.filter(user__identification=self.cleaned_data['identification']).exists()
# #         if existing_student:
# #             raise ValidationError('This identification number is already in use. Please enter a unique value.')
# #         return self.cleaned_data['identification']

# #     def clean_student_number(self):
# #         """Custom validation method for student_number field."""
# #         existing_student = Student.objects.filter(user__student_number=self.cleaned_data['student_number']).exists()
# #         if existing_student:
# #             raise ValidationError('This student number is already in use. Please enter a unique value.')
# #         return self.cleaned_data['student_number']


# # class StudentLeader(Student):
# #     is_student_leader = models.BooleanField(default=True)










# # # Custom User Manager
# # class UserManager(BaseUserManager):
# #     def create_user(self, email, password, **extra_fields):
# #         if not email:
# #             raise ValueError('The email must be set')
# #         email = self.normalize_email(email)
# #         user = self.model(email=email, **extra_fields)
# #         user.set_password(password)
# #         user.save(using=self._db)
# #         return user

# #     def create_superuser(self, email, password, **extra_fields):
# #         extra_fields.setdefault('is_staff', True)
# #         extra_fields.setdefault('is_superuser', True)
# #         return self.create_user(email, password, **extra_fields)

    
# # # Custom User Model
# # class CustomUser(AbstractBaseUser, PermissionsMixin):
# #     email = models.EmailField(unique=True)
# #     is_staff = models.BooleanField(default=False)
# #     is_active = models.BooleanField(default=True)
# #     date_joined = models.DateTimeField(default=timezone.now)

# #     # Add related_name arguments to avoid conflicts
# #     groups = models.ManyToManyField(
# #         'auth.Group',
# #         related_name='customuser_set',  # Changed related_name here
# #         blank=True,
# #         help_text='The groups this user belongs to. A user can belong to multiple groups.',
# #         verbose_name='groups'
# #     )
# #     user_permissions = models.ManyToManyField(
# #         'auth.Permission',
# #         related_name='customuser_set',  # Changed related_name here
# #         blank=True,
# #         help_text='Specific permissions for this user.',
# #         verbose_name='user permissions'
# #     )

# #     USERNAME_FIELD = 'email'
# #     REQUIRED_FIELDS = []

# #     objects = UserManager()


# #     def __str__(self):
# #         return self.email

# # class Student(models.Model):
# #     # Step 1
# #     GENDER_CHOICES = [
# #         ('male', 'Male'),
# #         ('female', 'Female'),
# #         ('other', 'Other'),
# #     ]
# #     APPLICATION_STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('accepted', 'Accepted'),
# #         ('rejected', 'Rejected'),
# #     ]

# #     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
# #     full_name = models.CharField(max_length=100)
# #     email = models.EmailField(unique=True)
# #     phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+27 70 0000 000'. 10 digits allowed.")
# #     phone_number = models.CharField(validators=[phone_regex], max_length=15)
# #     student_number = models.CharField(max_length=20, unique=True)
# #     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
# #     identification = models.CharField(max_length=20, unique=True, null=False)

# #     # ADDITIONAL DETAILS
# #     is_accepted = models.BooleanField(default=False)
# #     application_status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
# #     date_of_birth = models.DateField(blank=True, null=True)
# #     course = models.CharField(max_length=100, blank=True, null=True)
# #     sponsor_details = models.TextField(null=True, blank=True)
# #     room_type = models.CharField(max_length=50, null=True, blank=True)
# #     next_of_kin_full_name = models.CharField(max_length=100, null=True, blank=True)
# #     next_of_kin_address = models.CharField(max_length=200, null=True, blank=True)
# #     next_of_kin_contact = models.CharField(max_length=20, null=True, blank=True)
# #     next_of_kin_identification = models.CharField(max_length=20, null=True, blank=True)

# #     class Meta:
# #         verbose_name = "Student"
# #         verbose_name_plural = "Students"

# #     def __str__(self):
# #         return self.full_name

# #     def clean_identification(self):
# #         """Custom validation method for identification field."""
# #         existing_student = Student.objects.filter(identification=self.cleaned_data['identification']).exists()
# #         if existing_student:
# #             raise ValidationError('This identification number is already in use. Please enter a unique value.')
# #         return self.cleaned_data['identification']

# #     def clean_student_number(self):
# #         """Custom validation method for student_number field."""
# #         existing_student = Student.objects.filter(student_number=self.cleaned_data['student_number']).exists()
# #         if existing_student:
# #             raise ValidationError('This student number is already in use. Please enter a unique value.')
# #         return self.cleaned_data['student_number']






















# # from django.db import models
# # from django.core.validators import RegexValidator
# # import uuid
# # from django.core.exceptions import ValidationError
# # from django.contrib.auth.models import User


# # class Student(models.Model):
# #     #Step 1
# #     GENDER_CHOICES = [
# #         ('male', 'Male'),
# #         ('female', 'Female'),
# #         ('other', 'Other'),
# #     ]
# #     APPLICATION_STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('accepted', 'Accepted'),
# #         ('rejected', 'Rejected'),
# #     ]

# #     full_name = models.CharField(max_length=100)
# #     email = models.EmailField(unique=True)
# #     phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+27 70 0000 000'. 10 digits allowed.")
# #     phone_number = models.CharField(validators=[phone_regex], max_length=15)
# #     student_number = models.CharField(max_length=20, unique=True)
# #     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
# #     identification = models.CharField(max_length=20, unique=True, null=False)


# #     #Step 2
# #     # User Integration (Step 2)
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)  # Link to the User model


# #     # ADDITIONAL DETAILS
# #     is_accepted = models.BooleanField(default=False)    
# #     application_status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')
# #     date_of_birth = models.DateField(blank=True, null=True)
# #     course = models.CharField(max_length=100, blank=True, default='Unknown')
# #     sponsor_details = models.TextField(null=True, blank=True)
# #     room_type = models.CharField(max_length=50, null=True, blank=True)
# #     next_of_kin_full_name = models.CharField(max_length=100, null=True, blank=True)
# #     next_of_kin_address = models.CharField(max_length=200, null=True, blank=True)
# #     next_of_kin_contact = models.CharField(max_length=20, null=True, blank=True)
# #     next_of_kin_identification = models.CharField(max_length=20, null=True, blank=True)

# #     class Meta:
# #         verbose_name = "Student"
# #         verbose_name_plural = "Students"

# #     def __str__(self):
# #         return self.full_name
    
# #     def clean_identification(self):
# #         """Custom validation method for identification field."""
# #         existing_student = Student.objects.filter(identification=self.cleaned_data['identification']).exists()
# #         if existing_student:
# #             raise ValidationError('This identification number is already in use. Please enter a unique value.')
# #         return self.cleaned_data['identification']
    
# #     def clean_student_number(self):
# #         """Custom validation method for student_number field."""
# #         existing_student = Student.objects.filter(student_number=self.cleaned_data['student_number']).exists()
# #         if existing_student:
# #             raise ValidationError('This student number is already in use. Please enter a unique value.')
# #         return self.cleaned_data['student_number']