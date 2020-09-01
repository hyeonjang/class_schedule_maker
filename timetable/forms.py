import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from school.models import Term
from .models import TimeTable, ClassRoom

class WeekSelectForm(forms.Form):
  week = forms.DateField(widget = forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'week'}))

class TermSelectForm(forms.Form):
  week = forms.DateField(widget = forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'week'}))

class TimeTableForm(forms.ModelForm):
  class Meta:
    model = TimeTable
    fields = ['classRoom', 'subject', 'semester', 'weekday', 'time']

TimeTableCreateFormset = inlineformset_factory(User, TimeTable, extra=40, form=TimeTableForm)
TimeTableUpdateFormset = inlineformset_factory(User, TimeTable, extra=0, form=TimeTableForm)

