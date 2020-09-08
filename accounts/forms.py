from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction

from .models import User, HomeTeacher, SubjectTeacher
from school.models import Subject, ClassRoom
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class SubjectSignUpForm(UserCreationForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.SUBJECT
        user.save()
        subjectt = SubjectTeacher.objects.create(user=user)
        subjectt.subject.add(*self.cleaned_data.get('subject'))
        return user

class HomeroomSignUpForm(UserCreationForm):
    classroom = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), required=True)

    class Meta(UserCreationForm.Meta):
        model = User

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

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
