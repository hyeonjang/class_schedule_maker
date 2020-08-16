from django import forms
from .models import TimeTable

class SubjectTableForm(forms.Form):
   #c_weekday = forms.CharField(max_length=64, required=False)
   #i_time = forms.IntegerField(required=False)
   classNumber = forms.IntegerField(required=False)
   subject = forms.CharField(max_length=64, required=False)
