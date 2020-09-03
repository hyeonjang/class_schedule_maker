from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from school.models import ClassRoom, Subject
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    classRoom = forms.ModelChoiceField(queryset=ClassRoom.objects.all())

    class Meta:
        model = User
        fields = ('email', 'name', 'classRoom')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 
            'is_homeroom', 
            'classRoom', 
            'is_subject', 'assigned_subjects_number',
            'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6'
        ]

    def clean_password(self):
        return self.initial["password"]
    
    def clean(self):
        cleaned_data = super().clean()
        
        is_homeroom = cleaned_data.get("is_homeroom")
        is_subject = cleaned_data.get("is_subject")

        classRoom = cleaned_data.get("classRoom")

        assigned = cleaned_data.get("assigned_subjects_number")
        
        subject_list = []
        subject1 = cleaned_data.get("subject1")
        subject2 = cleaned_data.get("subject2")
        subject3 = cleaned_data.get("subject3")
        subject4 = cleaned_data.get("subject4")
        subject5 = cleaned_data.get("subject5")
        subject6 = cleaned_data.get("subject6")

        if subject1 is not None:
            subject_list.append(subject1)
        if subject2 is not None:
            subject_list.append(subject2)
        if subject3 is not None:
            subject_list.append(subject3)
        if subject4 is not None:
            subject_list.append(subject4)
        if subject5 is not None:
            subject_list.append(subject5)
        if subject6 is not None:
            subject_list.append(subject6)

        # role set
        if is_homeroom and is_subject:
            raise ValidationError("Must select one role")

        if is_homeroom and classRoom is None:
            raise ValidationError("You must choose your classRoom")

        if is_subject and subject1 is None:
            raise ValidationError("")

        if is_subject and (assigned != len(subject_list)):
            error_message = f"Please set correctly subjects! you are assigned {assigned}, but you choose"

            for subject in subject_list:
                error_message += " " + subject.to_string()

            raise ValidationError(error_message)