'''
School Information Form
'''
from django import forms
from django.core.exceptions import ValidationError

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from accounts.models import User
from .models import Term, Holiday, ClassRoom, Subject

class TimeTableCreation(forms.Form):
    semester = forms.ModelChoiceField(Term.objects.all())
    classroom = forms.ModelChoiceField(ClassRoom.objects.all(), required=False)
    teacher = forms.ModelChoiceField(User.objects.all(), required=False)

    def clean(self):
        classroom = self.cleaned_data.get('classroom')
        teacher = self.cleaned_data.get('teacher')

        if classroom and teacher:
            raise ValidationError('please select classroom or subject')
        
        if classroom is None and teacher is None:
            raise ValidationError('please select classroom or subject')

class TermModelForm(BSModalModelForm):
    class Meta:
        model = Term
        fields = '__all__'

class HolidayModelForm(BSModalModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
          'day': forms.DateInput()
        }

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

