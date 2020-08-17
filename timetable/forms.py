from django import forms
from .models import TimeTable

class SubjectTableForm(forms.Form):
   #c_weekday = forms.CharField(max_length=64, required=False)
   #i_time = forms.IntegerField(required=False)
   classNumber = forms.IntegerField(initial=0,required=False)
   subject = forms.CharField(initial="sc", max_length=64, required=False)
   weekday = forms.CharField(max_length=64)

   def init(self, n, s):
      self.classNumber = n
      self.subject = s
