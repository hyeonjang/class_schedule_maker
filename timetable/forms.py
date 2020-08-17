from django import forms
from .models import TimeTable

class SubjectTableForm(forms.Form):
   id = forms.IntegerField() ## for debugging
   classNumber = forms.IntegerField(required=False)
   time = forms.IntegerField()
   subject = forms.CharField(max_length=64, required=False)
   weekday = forms.CharField(max_length=64)