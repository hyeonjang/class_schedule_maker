'''
doc
'''
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from bootstrap_modal_forms.generic import BSModalCreateView
from accounts.models import User
from .forms import SubjectPopForm, HomeroomPopForm, InvitedPopForm, HomeroomProfileForm, SubjectProfileForm, InvitedProfileForm

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

@login_required
def homeroomProfileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = HomeroomProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('account:login'))
    else:
        form = HomeroomProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})

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

@login_required
def subjectProfileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = SubjectProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = SubjectProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})


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

@login_required
def invitedProfileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = InvitedProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = InvitedProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})

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
