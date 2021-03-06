'''
modul doc
'''
from django import forms
from django.forms import inlineformset_factory
from bootstrap_modal_forms.forms import BSModalForm
from accounts.models import User
from school.models import Term, ClassRoom, Subject
from .models import SubjectTable, HomeTable, Invited

class SubjectTableForm(forms.ModelForm):
    '''
    class doc
    '''
    class Meta:
        model = SubjectTable
        fields = ['classroom', 'subject']

    def __init__(self, *args, **kwargs):
        super(SubjectTableForm, self).__init__(*args, **kwargs)
        if isinstance(kwargs['instance'], self.Meta.model):
            # 0. disable
            if kwargs['instance'].is_event_or_holi:
                for field in self.fields.values():
                    field.widget.attrs.update({'disabled':'true'})
                return
            # 1. choose the hometable which has not sub_teacher that class time
            class_list = HomeTable.objects.filter(day=kwargs['instance'].day, time=kwargs['instance'].time, inv_teacher=None).distinct('classroom').values_list('classroom', flat=True)
            self.fields['classroom'] = forms.ModelChoiceField(queryset=ClassRoom.objects.filter(pk__in=class_list), required=False)
            # 2. filter subject
            self.fields['subject'] = forms.ModelChoiceField(queryset=Subject.objects.filter(pk__in=kwargs['instance'].teacher.return_by_type().subject.all()), required=False)

class HomeTableForm(forms.ModelForm):
    '''
    class doc
    '''
    auto = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    class Meta:
        model = HomeTable
        fields = ['auto', 'subject']

    def __init__(self, *args, **kwargs):
        super(HomeTableForm, self).__init__(*args, **kwargs)
        if isinstance(kwargs['instance'], self.Meta.model):
            # 0. disable
            if kwargs['instance'].is_event_or_holi:
                for field in self.fields.values():
                    field.widget.attrs.update({'disabled':'true'})
                return
            # 1. fields update
            hometeacher = kwargs['instance'].teacher.return_by_type()
            self.fields['subject'] = forms.ModelChoiceField(queryset=Subject.objects.filter(grade=hometeacher.get_grade()), required=False)

            # 2. disable to select subject when other teacher already exists
            if kwargs['instance'].sub_teacher or kwargs['instance'].inv_teacher:
                self.fields['subject'].widget.attrs.update({'disabled':'true'})
                self.fields['auto'].widget.attrs.update({'disabled':'true'})

    def is_disabled(self):
        if self.fields['subject'].widget.attrs:
            if self.fields['subject'].widget.attrs['disabled']:
                return True
        return False

class InvitedTableForm(forms.ModelForm):
    '''
    class doc
    '''
    class Meta:
        model = Invited
        fields = ['classroom', 'subject']

    def __init__(self, *args, **kwargs):
        super(InvitedTableForm, self).__init__(*args, **kwargs)
        if isinstance(kwargs['instance'], self.Meta.model):
            # 0. disable
            if kwargs['instance'].is_event_or_holi:
                for field in self.fields.values():
                    field.widget.attrs.update({'disabled':'true'})
                return
            # 1. choose the hometable which has not inv_teacher that class time
            class_list = HomeTable.objects.filter(day=kwargs['instance'].day, time=kwargs['instance'].time, sub_teacher=None).distinct('classroom').values_list('classroom', flat=True)
            self.fields['classroom'] = forms.ModelChoiceField(queryset=ClassRoom.objects.filter(pk__in=class_list), required=False)

class TableCreateForm(BSModalForm):
    semester = forms.ModelChoiceField(queryset=Term.objects.all())

SubjectTableUpdateFormset = inlineformset_factory(User, SubjectTable, extra=0, form=SubjectTableForm, can_delete=False)
HomeTableUpdateFormset = inlineformset_factory(User, HomeTable, fk_name='teacher', extra=0, form=HomeTableForm, can_delete=False)
InvitedTableUpdateFormset = inlineformset_factory(User, Invited, extra=0, form=InvitedTableForm, can_delete=False)
