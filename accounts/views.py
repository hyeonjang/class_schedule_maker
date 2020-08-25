from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from . import models, forms

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('home')
    else:
        form = forms.SignUpForm()
    return render(request, 'accounts/signup.html', {'form':form })

def login(request):
    if request.POST:
        form = forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            form.add_error(None, 'invalid Username or Password')
    else:
        form = forms.LoginForm()
    return render(request, 'accounts/login.html', {'form':form })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('home')