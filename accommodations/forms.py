from django import forms
from .models import Room, RoomInspectionRequest, MaintenanceRequest, RoomReservation, Complaint

class InspectionRequestForm(forms.ModelForm):
    class Meta:
        model = RoomInspectionRequest
        fields = ['inspection_date', 'room']
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ('room', 'location', 'description', 'urgency')

    def __init__(self, *args, **kwargs):
        super(MaintenanceRequestForm, self).__init__(*args, **kwargs)
        # Dynamically populate the room field based on the currently logged-in user
        user = kwargs.get('user')
        if user:
            self.fields['room'].queryset = Room.objects.filter(student=user)

    def clean(self):
        cleaned_data = super(MaintenanceRequestForm, self).clean()
        room = cleaned_data.get('room')
        location = cleaned_data.get('location')

        # Ensure either room or location is provided, but not both
        if room and location:
            raise forms.ValidationError("Please specify either a room or a common area location, not both.")
        elif not room and not location:
            raise forms.ValidationError("Please specify either the room or the common area location for the maintenance request.")

        return cleaned_data


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category']


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