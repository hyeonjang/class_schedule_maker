'''
doc
'''
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView
from .forms import SubjectPopForm, HomeroomPopForm, InvitedPopForm, CustomAuthenticationForm

class HomeroomSignUpView(BSModalCreateView):
    form_class = HomeroomPopForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')

class SubjectSignUpView(BSModalCreateView):
    form_class = SubjectPopForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('')

class InvitedSignUpView(BSModalCreateView):
    form_class = InvitedPopForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('')

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'index.html'
    success_message = 'Success: You were successfully logged in.'

    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    return redirect('index')