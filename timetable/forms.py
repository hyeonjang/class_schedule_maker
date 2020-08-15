from django import forms
from .models import TimeTable

class TableForm(forms.ModelForm):
   classNumber = forms.IntegerField(required=False)

   class Meta:
        model = TimeTable
        fields = ['c_teacher', 'classNumber']