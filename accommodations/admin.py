from django.contrib import admin
from .models import Room, RoomInspectionRequest, MaintenanceRequest, Building, StudentAllocation, RoomReservation, Complaint, VisitorLog
from .models import Payment, LeaseAgreement, Bursary
from accounts.models import CustomUser
from accounts.admin import CustomUserAdmin as AccountsCustomUserAdmin  # Import the original CustomUserAdmin
from .forms import PaymentMethodForm  # Import the PaymentForm

# @admin.action(description='Allocate rooms to accepted students')
# def allocate_rooms(modeladmin, request, queryset):
#     for student in queryset:
#         # Find an available room based on the student's gender
#         available_rooms = Room.objects.filter(
#             building__gender=student.gender,
#             capacity__gt=Room.objects.filter(occupants=student).count()
#         ).order_by('capacity')

#         if available_rooms:
#             room = available_rooms.first()
#             StudentAllocation.objects.create(student=student, room=room)

@admin.action(description='Allocate rooms to accepted students')
def allocate_rooms(modeladmin, request, queryset):
    for student in queryset:
        print(student)
        # Find an available room based on the student's gender
        available_rooms = Room.objects.filter(
            building__gender_type=student.gender,
            capacity__gt=Room.objects.filter(occupants=student).count()
        ).order_by('capacity')

        print(available_rooms)
        if available_rooms:
            room = available_rooms.first()
            room.occupants.add(student)
            StudentAllocation.objects.create(student=student, room=room)
            print("Added to room!")




class CustomUserAdmin(AccountsCustomUserAdmin):  # Inherit from the original CustomUserAdmin
    actions = [allocate_rooms]

    
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentMethodForm
    list_display = ('rental_agreement', 'amount', 'payment_date', 'paid_by_bursary', 'is_cash_payment')
    list_filter = ('paid_by_bursary', 'is_cash_payment')
    search_fields = ('rental_agreement__student__email', 'bursary__name', 'cash_payment_reference', 'bursary_reference_number')

    def get_fields(self, request, obj=None):
        fields = ['rental_agreement', 'amount', 'payment_date', 'paid_by_bursary', 'is_cash_payment']
        if obj:
            if obj.is_cash_payment:
                fields += ['cash_payment_reference', 'cash_payment_date', 'cash_payment_method']
            if obj.paid_by_bursary:
                fields += ['bursary', 'bursary_name', 'bursary_reference_number', 'bursary_payment_date', 'bursary_contact_information', 'bursary_terms_and_conditions', 'bursary_agreement_document']
        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.is_cash_payment:
                return ['paid_by_bursary', 'bursary', 'bursary_name', 'bursary_reference_number', 'bursary_payment_date', 'bursary_contact_information', 'bursary_terms_and_conditions', 'bursary_agreement_document']
            if obj.paid_by_bursary:
                return ['is_cash_payment', 'cash_payment_reference', 'cash_payment_date', 'cash_payment_method']
        return []


# Unregister the original CustomUser admin and register the new one
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Payment)
admin.site.register(Bursary)
admin.site.register(LeaseAgreement)
admin.site.register(RoomInspectionRequest)
admin.site.register(MaintenanceRequest)
admin.site.register(StudentAllocation)
admin.site.register(RoomReservation)
admin.site.register(Complaint)
admin.site.register(VisitorLog)
