from django import forms
from .models import TimeTable

class SubjectTableForm(forms.Form):
   id = forms.IntegerField() ## for debugging
   classNumber = forms.IntegerField(required=False)
   time = forms.IntegerField(required=False)
   subject = forms.CharField(max_length=64, required=False)
   weekday = forms.CharField(max_length=64)

   def set_values(self, classNumber, time, subject, weekday, *args, **kwargs):
      self.classNumber = classNumber
      self.time = time
      self.subject = subject
      self.weekday = weekday

class TableForm(forms.ModelForm):
   id = forms.IntegerField()
   subject = forms.CharField(max_length=64, required=False)

   class Meta:
      model = TimeTable
      fields = ['id', 'classNumber', 'subject']
   
   # def clean_subject(self):
   #    if self.cleaned_data['subject'] != None:
   #       print(self.cleaned_data['subject'])

   #    subject = self.cleaned_data['subject']
   #    if subject == None:
   #       print("invalid")

   #    return subject
     