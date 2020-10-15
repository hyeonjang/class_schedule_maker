'''
doc
'''
from django.contrib.auth import login, logout
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
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        if not self.request.is_ajax(): #bug in django-bootstrap-modal-form
            form.save()
        return redirect(self.success_url)

class SubjectSignUpView(BSModalCreateView):
    '''
    inherited
    '''
    form_class = SubjectPopForm
    template_name = 'signup.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        if not self.request.is_ajax(): #bug in django-bootstrap-modal-form
            form.save()
        return redirect(self.success_url)

class InvitedSignUpView(BSModalCreateView):
    '''
    inherited
    '''
    form_class = InvitedPopForm
    template_name = 'signup.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        if not self.request.is_ajax(): #bug in django-bootstrap-modal-form
            form.save()
        return redirect(self.success_url)

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
    return redirect('account:login')
