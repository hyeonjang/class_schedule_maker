from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from school.models import ClassRoom, Subject
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', )

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
            'is_subject',            
        ]

    def clean_password(self):
        return self.initial["password"]
    
    def clean(self):
        cleaned_data = super().clean()
        
        is_homeroom = cleaned_data.get("is_homeroom")
        is_subject = cleaned_data.get("is_subject")

        # role set
        if is_homeroom and is_subject:
            raise forms.ValidationError("Must select one role")

        if not is_homeroom and not is_subject:
            raise forms.ValidationError("You must choose your role")

