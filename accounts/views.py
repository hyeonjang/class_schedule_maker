'''
doc
'''
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView
from .forms import SubjectPopForm, HomeroomPopForm, InvitedPopForm

class HomeroomSignUpView(BSModalCreateView):
    '''
    inherited
    '''
    form_class = HomeroomPopForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('timetable:home_view')

    def form_valid(self, form):
        if self.request.is_ajax():
            form.save()
        return redirect('login')

class SubjectSignUpView(BSModalCreateView):
    '''
    inherited
    '''
    form_class = SubjectPopForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        print(redirect(reverse_lazy('home')))
        return reverse_lazy('home')

class InvitedSignUpView(BSModalCreateView):
    '''
    inherited
    '''
    form_class = InvitedPopForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    '''
    inherited
    '''
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    '''
    logout view
    '''
    logout(request)
    return redirect('login')
