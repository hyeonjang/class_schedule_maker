'''
modul doc
'''
from django import forms
from django.forms import inlineformset_factory

from accounts.models import User, SubjectTeacher, HomeTeacher
from .models import TimeTable, SubjectTable, HomeTable

class TimeTableForm(forms.ModelForm):
    '''
    class doc
    '''
    class Meta:
        model = TimeTable
        fields = ['classroom', 'subject']

class SubjectTableForm(forms.ModelForm):
    '''
    class doc
    '''
    class Meta:
        model = SubjectTable
        fields = ['classroom', 'subject']

class HomeTableForm(forms.ModelForm):
    '''
    class doc
    '''
    sub_teacher = forms.ModelChoiceField(queryset=SubjectTeacher.objects.all())
    class Meta:
        model = HomeTable
        fields = ['subject', 'sub_teacher']

    def __init__(self, *args, **kwargs):
        super(HomeTableForm, self).__init__(*args, **kwargs)
        
        print(self.fields.keys())
        self.fields['subject'].widget.attrs.update({'disabled':'true'})
        self.fields['sub_teacher'].widget.attrs.update({'disabled':'true'})

SubjectTableCreateFormset = inlineformset_factory(User, SubjectTable, extra=40, form=SubjectTableForm, can_delete=False)
SubjectTableUpdateFormset = inlineformset_factory(User, SubjectTable, extra=0, form=SubjectTableForm, can_delete=False)
HomeTableCreateFormset = inlineformset_factory(User, HomeTable, fk_name='teacher', extra=40, form=HomeTableForm, can_delete=False)
HomeTableUpdateFormset = inlineformset_factory(User, HomeTable, fk_name='teacher', extra=0, form=HomeTableForm, can_delete=False)
