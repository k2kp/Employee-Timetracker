from django import forms
from .models import TimeEntry
from .models import Project

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['project', 'start_time', 'end_time','duration']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']