'''
doc
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

from school.models import Subject, ClassRoom
from .models import User, HomeTeacher, SubjectTeacher, InvitedTeacher

class HomeroomPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    classroom = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.HOMEROOM
        user.save()
        HomeTeacher.objects.create(
            user=user,
            classroom=self.cleaned_data.get('classroom'),
        )
        return user

class SubjectPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class':'form-check-input'})

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.SUBJECT
        user.save()
        subjectt = SubjectTeacher.objects.create(user=user)
        subjectt.subject.add(*self.cleaned_data.get('subject'))
        return user

class InvitedPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    start = forms.DateField(input_formats=['%Y/%m/%d'],
                            widget=forms.SelectDateWidget)
    end = forms.DateField(input_formats=['%Y/%m/%d'],
                            widget=forms.SelectDateWidget)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.INVITED
        user.save()
        subjectt = InvitedTeacher.objects.create(user=user)
        subjectt.subject.add(*self.cleaned_data.get('subject'))
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
