"""
module doc
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.shortcuts import redirect

from django.views import generic
from django.urls import reverse_lazy

from accounts.models import HomeTeacher
from school.models import Term

from .models import SubjectTable, HomeTable, Invited
from .forms import (SubjectTableForm, HomeTableForm, SubjectTableCreateFormset, SubjectTableUpdateFormset, HomeTableCreateFormset, HomeTableUpdateFormset)

##########################################################
### Teacher Roles == Subject Features
class SubjectCreate(LoginRequiredMixin, generic.CreateView): # actullay update instances
    '''
    class doc
    '''
    template_name = 'sub_create.html'
    model = SubjectTable
    form_class = SubjectTableForm

    def get_success_url(self):
        return reverse_lazy('timetable:sub_view', kwargs={'user_id': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super(SubjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SubjectTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['formset'] = SubjectTableCreateFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.objects.get(pk=1)
        week = semester.get_starting_week()
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.semester = semester
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = week[i%5]
                instance.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class SubjectUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'sub_update.html'
    model = SubjectTable
    form_class = SubjectTableForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('timetable:sub_view', kwargs={'user_id': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super(SubjectUpdate, self).get_context_data(**kwargs)
        qs = SubjectTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04"))
        if self.request.POST:
            context['TimeTables'] = SubjectTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['TimeTables'] = SubjectTableUpdateFormset(instance=self.request.user, queryset=qs)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['TimeTables']
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                instance.save()
                #if instance.classroom and instance.subject:
                #    copy_sub_to_home(instance)
            messages.success(self.request, 'success', extra_tags='alert')
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['TimeTables']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class SubjectView(LoginRequiredMixin, generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'sub_view.html'
    model = SubjectTable

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:sub_view')

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['TimeTables'] = SubjectTable.objects.filter(
            teacher=self.request.user,
            weekday__range=("2020-08-31", "2020-09-04")
            ).order_by("time", "weekday")
        # print(context['TimeTables'])
        return context

### the end of subject
##########################################################
##########################################################
### instatiate HomeRoom TimeTable model for Semester in django admin

##########################################################
### Teacher Roles == Homeroom Features
class HomeRoomCreate(generic.CreateView):
    '''
    class doc
    '''
    template_name = 'home_create.html'
    model = HomeTable
    form_class = HomeTableForm

    def get_success_url(self):
        return reverse_lazy('timetable:home_view', kwargs={'user_id':self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super(HomeRoomCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = HomeTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['formset'] = HomeTableCreateFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.objects.get(pk=1)
        week = semester.get_starting_week()
        #weeks = semester.end.isocalendar()[1] - semester.start.isocalendar()[1]
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.classroom = HomeTeacher.objects.get(user=self.request.user).classroom
                instance.semester = semester
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = week[i%5]
                instance.save()
                #expand_inst_to_term(instance, week[i%5], weeks)
            messages.success(self.request, 'success', extra_tags='alert')
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class HomeRoomUpdate(generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'home_update.html'
    model = HomeTable
    form_class = HomeTableForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(HomeRoomUpdate, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04"))
        if self.request.is_ajax:
            startdate = self.request.GET.get('startdate')
            enddate = self.request.GET.get('enddate')
            if startdate and enddate:
                startdate = startdate[0:10] # iso format
                enddate = enddate[0:10]
                print(startdate, enddate)
                qs = HomeTable.objects.filter(teacher=self.request.user, weekday__range=(startdate, enddate))

        if self.request.POST:
            context['TimeTables'] = HomeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['TimeTables'] = HomeTableUpdateFormset(instance=self.request.user, queryset=qs)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['TimeTables']
        if formset.is_valid():
            formset.save()
            messages.success(self.request, 'success', extra_tags='alert')
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['TimeTables']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class HomeRoomView(generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'home_view.html'
    model = HomeTable

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:home_view')

    def get_context_data(self, **kwargs):
        context = super(HomeRoomView, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04")).order_by("time", "weekday")
        context['TimeTables'] = qs
        return context

##########################################################
### Teacher Roles == Invited
class InvitedView(generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'invited_view.html'
    model = HomeTable

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:invited_view')

    def get_context_data(self, **kwargs):
        context = super(InvitedView, self).get_context_data(**kwargs)
        qs = Invited.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04")).order_by("time", "weekday")
        context['TimeTables'] = qs
        return context
