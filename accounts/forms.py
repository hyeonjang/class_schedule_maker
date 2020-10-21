'''
doc
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
import school
from .models import User, HomeTeacher, SubjectTeacher, InvitedTeacher

class HomeroomPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    '''
    SignUp Homeroom Teahcer Popup Form
    '''
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'school', 'grade']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.HOMEROOM
        user.save()
        HomeTeacher.objects.create(user=user, classroom=self.cleaned_data.get('classroom'),)
        return user

class HomeroomProfileForm(forms.ModelForm):
    '''
    Profile for Homeroom Teacher
    '''
    classroom = forms.ModelChoiceField(queryset=school.models.ClassRoom.objects.all())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'school', 'grade', ]

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.set_password(user.password)
        user.save()
        home = user.return_by_type()
        home.classroom = self.cleaned_data.get('classroom')
        home.save()
        return user

class SubjectPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    '''
    SignUp Subject Teahcer Popup Form
    '''
    subject = forms.ModelMultipleChoiceField(queryset=school.models.Subject.objects.all(), required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'school', 'grade']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.SUBJECT
        user.save()
        sub = SubjectTeacher.objects.create(user=user)
        sub.subject.add(*self.cleaned_data.get('subject'))
        return user

class SubjectProfileForm(forms.ModelForm):
    '''
    Profile for Subject Teacher
    '''
    subject = forms.ModelMultipleChoiceField(queryset=school.models.Subject.objects.all(), required=False)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'school', 'grade', ]

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.set_password(user.password)
        user.save()
        sub = user.return_by_type()
        sub.subject.clear()
        sub.subject.add(*self.cleaned_data.get('subject'))
        return user

class InvitedPopForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    '''
    SignUp Invited Teahcer Popup Form
    '''

    start = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    end = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'school', 'grade']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.INVITED
        user.save()
        InvitedTeacher.objects.create(user=user, start=self.cleaned_data.get('start'), end=self.cleaned_data.get('end'))
        return user

class InvitedProfileForm(forms.ModelForm):
    '''
    Profile for Invited Teacher
    '''
    start = forms.DateField()
    end = forms.DateField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'school', 'grade', ]

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.set_password(user.password)
        user.save()
        inv = user.return_by_type()
        inv.start = self.cleaned_data.get('start')
        inv.end = self.cleaned_data.get('end')
        inv.save()
        return user