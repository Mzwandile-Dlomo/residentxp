from django import forms
from .models import VisitorLog, Survey, Choice


class SurveyForm(forms.ModelForm):
    choices = forms.CharField(widget=forms.Textarea, help_text="Enter each choice on a new line.")

    class Meta:
        model = Survey
        fields = ['title', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        for choice_text in self.cleaned_data['choices'].splitlines():
            Choice.objects.create(survey=instance, text=choice_text)
        return instance


class VisitorLogForm(forms.ModelForm):
    class Meta:
        model = VisitorLog
        fields = ['visitor_name', 'visitor_contact', 'visit_purpose', 'visit_date']
        widgets = {
            'visit_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

