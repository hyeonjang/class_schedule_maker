'''
School Information Form
'''
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from accounts.models import User
from .models import Term, Holiday, ClassRoom, Subject

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
    teacher = forms.ModelChoiceField(User.objects.filter(user_type=User.HOMEROOM))

    class Meta:
        model = ClassRoom
        fields = '__all__'

class SubjectModelForm(BSModalModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

