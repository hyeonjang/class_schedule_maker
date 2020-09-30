'''
modul doc
'''
from django import forms
from django.forms import inlineformset_factory
from accounts.models import User
from school.models import ClassRoom, Subject
from .models import SubjectTable, HomeTable, Invited

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
    #sub_teacher = forms.ModelChoiceField(queryset=SubjectTeacher.objects.all())
    class Meta:
        model = HomeTable
        fields = ['subject']

    def __init__(self, *args, **kwargs):
        super(HomeTableForm, self).__init__(*args, **kwargs)
        #self.fields['subject'].widget.attrs.update({'disabled':'true'})
        #self.fields['sub_teacher'].widget.attrs.update({'disabled':'true'})

    def save(self, commit=True, create=False):
        instance = super(HomeTableForm, self).save(commit=False)
        if commit:
            instance.save(create=create)
        return instance

class InvitedTableForm(forms.ModelForm):
    '''
    class doc
    '''
    class Meta:
        model = Invited
        fields = ['classroom', 'subject']

    def __init__(self, *args, **kwargs):
        super(InvitedTableForm, self).__init__(*args, **kwargs)
        if isinstance(kwargs['instance'], Invited):
            class_list = HomeTable.objects.filter(day=kwargs['instance'].day, time=kwargs['instance'].time, sub_teacher=None).distinct('classroom').values_list('classroom', flat=True)
            self.fields['classroom'] = forms.ModelChoiceField(queryset=ClassRoom.objects.filter(pk__in=class_list), required=False)

SubjectTableCreateFormset = inlineformset_factory(User, SubjectTable, extra=40, form=SubjectTableForm, can_delete=False)
SubjectTableUpdateFormset = inlineformset_factory(User, SubjectTable, extra=0, form=SubjectTableForm, can_delete=False)
HomeTableCreateFormset = inlineformset_factory(User, HomeTable, fk_name='teacher', extra=40, form=HomeTableForm, can_delete=False)
HomeTableUpdateFormset = inlineformset_factory(User, HomeTable, fk_name='teacher', extra=0, form=HomeTableForm, can_delete=False)
InvitedTableUpdateFormset = inlineformset_factory(User, Invited, extra=0, form=InvitedTableForm, can_delete=False)
