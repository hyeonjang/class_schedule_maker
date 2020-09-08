from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalLoginView
from .forms import SubjectSignUpForm, HomeroomSignUpForm, CustomAuthenticationForm
from .models import User

class IndexView(TemplateView):
    template_name = 'index.html'

class SubjectSignUpView(CreateView):
    model = User
    form_class = SubjectSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'subject'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class HomeroomSignUpView(CreateView):
    model = User
    form_class = HomeroomSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'clasroom'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('home'))

def logout_view(request):
    logout(request)
    return redirect('index')