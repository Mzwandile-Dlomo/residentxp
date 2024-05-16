from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Payment, CustomUser, RentalAgreement, Bursary

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with additional fields."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'identification', 'gender')}),
        (_('User Type'), {'fields': ('user_type',)}),
        (_('Student Details'), {'fields': ('student_number', 'is_accepted', 'date_of_birth',
                                           'course',)}),
        (_('Next of keen'), {'fields': ('next_of_kin_full_name','next_of_kin_contact','next_of_kin_identification','next_of_kin_address',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'gender', 'identification', 'course', 'password1', 'password2'),
        }),
    )


    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'student_number')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if obj:  # editing an existing object
            return self.fieldsets
        else:  # adding a new object
            return self.add_fieldsets


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Payment)
admin.site.register(Bursary)
admin.site.register(RentalAgreement)
