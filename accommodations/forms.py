from django import forms
from .models import Room, RoomInspectionRequest, MaintenanceRequest

class InspectionRequestForm(forms.ModelForm):
    class Meta:
        model = RoomInspectionRequest
        fields = ['inspection_date', 'inspector', 'comments']
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
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