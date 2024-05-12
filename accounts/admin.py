from django.contrib import admin
from .models import Student, User, StudentLeader, Admin, RentalAgreement, Bursary

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentLeader)
admin.site.register(Admin)
admin.site.register(Bursary)
admin.site.register(RentalAgreement)