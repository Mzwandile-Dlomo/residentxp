from django import forms
from .models import RoomInspection

class InspectionRequestForm(forms.ModelForm):
    class Meta:
        model = RoomInspection
        fields = ['inspection_date', 'inspector', 'comments']
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
