from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
   
    #@@todo implement to bring school groups from modelbase
    TEMP_SCHOOL_CHOICES = (
        (1, 'primary'), 
    )

    school = forms.ChoiceField(choices=TEMP_SCHOOL_CHOICES)
    
    GROUP_CHOICES = (
        (1, 'homeroom'),
        (2, 'subject'),
        (3, 'instructor'),
        (4, 'head'),
    )
    
    Role = forms.ChoiceField(choices=GROUP_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')