from django import forms
from .models import Term, Holiday, ClassRoom, Subject

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class TermModelForm(forms.ModelForm):
  class Meta:
    model = Term
    fields = '__all__'

class HolidayModelForm(BSModalModelForm):
  class Meta:
    model = Holiday
    fields = '__all__'

class GradeFilterForm(BSModalForm):
  grade = forms.ChoiceField(choices=ClassRoom.GRADE_RANGE)
  
  class Meta:
    fields = ['grade', 'clear']

class ClassRoomModelForm(BSModalModelForm):
  class Meta:
    model = ClassRoom
    fields = '__all__'

class SubjectModelForm(BSModalModelForm):
  class Meta:
    model = Subject
    fields = '__all__'

