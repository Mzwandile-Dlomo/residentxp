from django import forms
from .models import Room, MaintenanceRequest, Complaint



class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ('location','room', 'description', 'urgency', 'picture')

    def __init__(self, *args, **kwargs):
        super(MaintenanceRequestForm, self).__init__(*args, **kwargs)
        # Dynamically populate the room field based on the currently logged-in user
        user = kwargs.get('user')
        if user:
            self.fields['room'].queryset = Room.objects.filter(student=user)

    def clean(self):
        cleaned_data = super(MaintenanceRequestForm, self).clean()
        location = cleaned_data.get('location')
        room = cleaned_data.get('room')

        
        # Ensure either room or location is provided, but not both
        if not room and location == 'room':
            raise forms.ValidationError("Please specify the room for the maintainance.")
        elif not room and not location:
            raise forms.ValidationError("Please specify either the room or the common area location for the maintenance request1.")
        elif location != 'room' and room:
            raise forms.ValidationError("Please specify either the room or the common area location for the maintenance request.")
        return cleaned_data


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category']
