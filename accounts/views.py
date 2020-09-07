from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.views import LoginView

from .forms import UserForm, UserCreationForm, UserChangeForm
from .models import User
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

class UserLogin(LoginView):           # 로그인
    template_name = 'login.html'
    success_url = '/'

    def form_invalid(self, form):
        return super().form_invalid(form)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('home')