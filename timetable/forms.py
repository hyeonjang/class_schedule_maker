import datetime

from django import forms
from django.forms import inlineformset_factory

from accounts.models import User
from school.models import Term
from .models import TimeTable, ClassRoom

class TimeTableForm(forms.ModelForm):
  class Meta:
    model = TimeTable
    fields = ['classRoom', 'subject', 'semester', 'weekday', 'time'] # DO NOT change
    
class TimeTableViewForm(forms.ModelForm):
  class Meta:
    model = TimeTable
    fields = '__all__'
    widgets = {
      'semester' : forms.HiddenInput(),
      'weekday' : forms.HiddenInput(),
      'time'    : forms.HiddenInput(),
      'created_time' : forms.HiddenInput(),
      'classRoom' : forms.Select(attrs={'disabled': True}),
      'subject' : forms.Select(attrs={'disabled': True}),
    }

TimeTableCreateFormset = inlineformset_factory(User, TimeTable, extra=40, form=TimeTableForm, can_delete=False)
TimeTableUpdateFormset = inlineformset_factory(User, TimeTable, extra=0, form=TimeTableForm, can_delete=False)
TimeTableViewFormset   = inlineformset_factory(User, TimeTable, extra=0, form=TimeTableViewForm, can_delete=False)

