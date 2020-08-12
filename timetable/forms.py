from django import forms
from .models import TimeTable

class TableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['teacher', 'classGrade']