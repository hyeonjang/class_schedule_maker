import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from school.models import Term
from .models import TimeTable, ClassRoom


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class TermSelectForm(forms.Form):
  CHOICE = [
    Term.objects.all()
  ]
  semester = forms.ChoiceField(choices=CHOICE)

class TimeTableForm(forms.ModelForm):
  class Meta:
    model = TimeTable
    fields = ['classRoom', 'subject', 'semester']

TimeTableInlineFormset = inlineformset_factory(User, TimeTable, extra=40, form=TimeTableForm)

