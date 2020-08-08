from django import forms

class LoginForm(forms.Form):
    userid = forms.CharField(label='id', max_length=20)
    userpwd = forms.CharField(label='pwd', max_length=50)