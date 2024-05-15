from django import forms
from .models import Room, RoomInspection, RoomItem

class RoomAssignmentForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['room'].queryset = Room.objects.filter(building__gender__in=['mixed', user.gender])

class RoomInspectionRequestForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['room'].queryset = user.rooms.all()

class RoomInspectionForm(forms.ModelForm):
    class Meta:
        model = RoomInspection
        fields = ['notes', 'items_present']

class RoomItemForm(forms.ModelForm):
    class Meta:
        model = RoomItem
        fields = ['name', 'description']