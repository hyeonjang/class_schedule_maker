from django import forms
from .models import TimeTable

class TableForm(forms.Form):
   c_weekday = forms.CharField(max_length=100, required=False)
   i_time = forms.IntegerField(required=False)
   classNumber = forms.IntegerField(required=False)
