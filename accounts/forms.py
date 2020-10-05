'''
doc
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import User, HomeTeacher, SubjectTeacher, InvitedTeacher

class HomeroomPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    '''
    SignUp Homeroom Teahcer Popup Form
    '''
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.HOMEROOM
        user.save()
        HomeTeacher.objects.create(user=user, classroom=self.cleaned_data.get('classroom'),)
        return user

class SubjectPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    '''
    SignUp Subject Teahcer Popup Form
    '''
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.SUBJECT
        user.save()
        SubjectTeacher.objects.create(user=user)
        #subjectt.subject.add(*self.cleaned_data.get('subject'))
        return user

class InvitedPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    '''
    SignUp Invited Teahcer Popup Form
    '''

    start = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    end = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.INVITED
        user.save()
        InvitedTeacher.objects.create(user=user, start=self.cleaned_data.get('start'), end=self.cleaned_data.get('end'))
        return user
