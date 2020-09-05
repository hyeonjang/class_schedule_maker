import datetime

from django import forms
from django.forms import inlineformset_factory

from accounts.models import User

from .models import School, Term, Subject, ClassRoom

from django.forms import inlineformset_factory

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class SchoolManageForm(forms.ModelForm):
  class Meta:
    model = School
    fields = '__all__'

class TermForm(forms.ModelForm):
  class Meta:
    model = Term
    fields = '__all__'

class SubjectModelForm(BSModalModelForm):
  class Meta:
    model = Subject
    fields = '__all__'

class ClassRoomForm(forms.ModelForm):
  class Meta:
    model = ClassRoom
    fields = '__all__'
