import base64
from django import forms
from .models import Room, RoomInspectionRequest, RoomReservation, LeaseAgreement, Payment
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
import re


class InspectionRequestForm(forms.ModelForm):
    class Meta:
        model = RoomInspectionRequest
        fields = ['inspection_date', 'room']
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
        }


class InspectionRequestFormManagement(forms.ModelForm):
    class Meta:
        model = RoomInspectionRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('Approved', 'Approved'),
                ('Rejected', 'Rejected'),
            ])
        }


class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['room', 'check_in_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(room_type__endswith='ensuite')
        self.instance.student = user


    def clean_room(self):
        room = self.cleaned_data['room']
        if not room.has_available_beds():
            raise forms.ValidationError("The selected room is already full.")
        # Check if the user has an existing pending or approved reservation for the same room
        existing_reservation = RoomReservation.objects.filter(
            student=self.instance.student,
            room=room,
            status__in=['pending', 'approved']
        ).exists()

        if existing_reservation:
            raise forms.ValidationError("You already have a reservation for this room.")

        return room
    


# class VisitorLogForm(forms.ModelForm):
#     class Meta:
#         model = VisitorLog
#         fields = ['visitor_name', 'visitor_contact', 'visit_purpose', 'visit_date']
#         widgets = {
#             'visit_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }



class LeaseAgreementForm(forms.ModelForm):

    class Meta:
        model = LeaseAgreement
        fields = ['semester', 'payment_frequency', 'signature']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['signature'].widget.attrs.update({'class': 'signature-field'})

    def clean(self):
        cleaned_data = super().clean()
        signature_data = self.data.get('signature')
        print(f"Received signature data: {signature_data}")

        if not signature_data:
            raise ValidationError("Lease agreement must be signed before saving.")
        else:
            # Extract the Base64 data using a regular expression
            base64_data = re.search(r'base64,(.*)', signature_data).group(1)
            
            # Create a ContentFile with the Base64-encoded data
            signature_file = ContentFile(base64.b64decode(base64_data))
            
            # Assign the signature file to the 'signature' field
            cleaned_data['signature'] = signature_file

        return cleaned_data



class RentalAgreementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate landlord choices from available rooms and buildings
        room_choices = [(room.building.name, room.building.name) for room in Room.objects.all()]
        self.fields['landlord'].widget.choices = room_choices

        # Populate rent amount choices similarly
        rent_amount_choices = []
        for room in Room.objects.all():
            rent_amount = room.get_rent_amount()
            rent_amount_choices.append((room.building.name, f"{rent_amount:.2f}"))
        self.fields['rent_amount'].widget.choices = rent_amount_choices
    
    class Meta:
        model = LeaseAgreement
        fields = ['landlord', 'rent_amount', 'payment_frequency', 'start_date', 'end_date']



class PaymentMethodForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = [
            'lease_agreement', 'amount', 'payment_date', 'paid_by_bursary', 'is_cash_payment',
            'cash_payment_reference', 'cash_payment_date', 'cash_payment_method',
            'bursary', 'bursary_name', 'bursary_reference_number', 'bursary_payment_date',
            'bursary_contact_information',
        ]

    def clean(self):
        cleaned_data = super().clean()
        paid_by_bursary = cleaned_data.get('paid_by_bursary')
        is_cash_payment = cleaned_data.get('is_cash_payment')

        if paid_by_bursary and is_cash_payment:
            raise forms.ValidationError("A payment cannot be both cash and bursary.")

        if is_cash_payment:
            if not cleaned_data.get('cash_payment_reference'):
                self.add_error('cash_payment_reference', "Cash payment reference must be provided for cash payments.")
            if not cleaned_data.get('cash_payment_date'):
                self.add_error('cash_payment_date', "Cash payment date must be provided for cash payments.")
            if not cleaned_data.get('cash_payment_method'):
                self.add_error('cash_payment_method', "Cash payment method must be provided for cash payments.")
        
        if paid_by_bursary:
            if not cleaned_data.get('bursary'):
                self.add_error('bursary', "Bursary must be selected for bursary payments.")
            if not cleaned_data.get('bursary_reference_number'):
                self.add_error('bursary_reference_number', "Bursary reference number must be provided for bursary payments.")
            if not cleaned_data.get('bursary_payment_date'):
                self.add_error('bursary_payment_date', "Bursary payment date must be provided for bursary payments.")

        return cleaned_data
    

# class SurveyForm(forms.ModelForm):
#     choices = forms.CharField(widget=forms.Textarea, help_text="Enter each choice on a new line.")

#     class Meta:
#         model = Survey
#         fields = ['title', 'description']

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if commit:
#             instance.save()
#         for choice_text in self.cleaned_data['choices'].splitlines():
#             Choice.objects.create(survey=instance, text=choice_text)
#         return instance