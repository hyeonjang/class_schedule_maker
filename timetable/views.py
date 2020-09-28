"""
module doc
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from school.models import Term
from school.models import Subject
from .models import SubjectTable, HomeTable, Invited
from .forms import (SubjectTableForm, HomeTableForm, InvitedTableForm, SubjectTableCreateFormset, SubjectTableUpdateFormset, HomeTableUpdateFormset, InvitedTableUpdateFormset)
from .utils import expand_to_term, create_list_for_weeks, create_information

##########################################################
### Teacher Roles == Subject Features
class SubjectCreate(LoginRequiredMixin, generic.CreateView): # actullay update instances
    '''
    class doc
    '''
    template_name = 'sub/create.html'
    model = SubjectTable
    form_class = SubjectTableForm

    def get_success_url(self):
        return reverse_lazy('timetable:sub_view', kwargs={'user_id': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super(SubjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['timetables'] = SubjectTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['timetables'] = SubjectTableCreateFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.objects.all().get()
        week = semester.get_starting_week()
        formset = context['timetables']
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
        formset = context['timetables']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class SubjectUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'sub/update.html'
    model = SubjectTable
    form_class = SubjectTableForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('timetable:sub_view', kwargs={'user_id': self.request.user.id})

    def get_context_data(self, **kwargs):
        semester = Term.get_current()
        week = semester.get_week()
        context = super(SubjectUpdate, self).get_context_data(**kwargs)
        qs = SubjectTable.objects.filter(teacher=self.request.user, weekday__range=(week[0].strftime("%Y-%m-%d"), week[4].strftime("%Y-%m-%d"))).order_by("time", "weekday")
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
    template_name = 'sub/view.html'
    model = SubjectTable

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:sub_view')

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['timetables'] = SubjectTable.objects.filter(
            teacher=self.request.user,
            weekday__range=("2020-08-31", "2020-09-04")
            ).order_by("time", "weekday")
        context['counts'] = SubjectTable.objects.filter(
            teacher=self.request.user,
            subject__in=Subject.objects.all(),
            ).count()
        return context
### the end of subject
##########################################################
### Teacher Roles == Homeroom Features
class HomeRoomCreate(LoginRequiredMixin, generic.UpdateView):
    '''
    @@todo actually update view to expand to whole semester
    '''
    template_name = 'home/create.html'
    model = HomeTable
    form_class = HomeTableForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        week = Term.get_current_week()
        start = week[0].strftime("%Y-%m-%d")
        end = week[4].strftime("%Y-%m-%d")
        return reverse_lazy('timetable:home_view', kwargs={'user_id':self.request.user.id, 'start':start, 'end':end})

    def get_context_data(self, **kwargs):
        semester = Term.get_current()
        week = semester.get_week()
        context = super(HomeRoomCreate, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(teacher=self.request.user, weekday__range=(week[0].strftime("%Y-%m-%d"), week[4].strftime("%Y-%m-%d")))
        if self.request.POST:
            context['timetables'] = HomeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = HomeTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = create_list_for_weeks()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.get_current() # todo
        week = semester.get_week()
        weeks = semester.get_count_of_weeks()
        #weeks = semester.end.isocalendar()[1] - semester.start.isocalendar()[1]
        formset = context['timetables']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.sememster = semester
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = week[i%5]
                instance.save()
                expand_to_term(instance, self.request.user, week[i%5], weeks) #@@todo
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class HomeRoomUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'home/update.html'
    model = HomeTable
    form_class = HomeTableForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(HomeRoomUpdate, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(teacher=self.request.user, weekday__range=(self.kwargs['start'], self.kwargs['end']))
        if self.request.POST:
            context['timetables'] = HomeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = HomeTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = create_list_for_weeks()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['timetables']
        if formset.is_valid():
            formset.save()
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class HomeRoomView(LoginRequiredMixin, generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'home/view.html'
    model = HomeTable


    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:home_view')

    def get_context_data(self, **kwargs):
        context = super(HomeRoomView, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(semester=Term.get_current(), teacher=self.request.user, weekday__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "weekday")
        context['timetables'] = qs
        context['list_weeks'] = create_list_for_weeks()
        context['information'] = create_information(self.request.user)

        return context
### the end of homeroom
##########################################################
### Teacher Roles == Invited
class InvitedView(generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'inv/view.html'
    model = HomeTable

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:inv_view')
    def get_context_data(self, **kwargs):
        context = super(InvitedView, self).get_context_data(**kwargs)
        qs = Invited.objects.filter(teacher=self.request.user, weekday__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "weekday")
        context['timetables'] = qs
        context['list_weeks'] = create_list_for_weeks()
        return context

class InvitedCreate(LoginRequiredMixin, generic.UpdateView):
    '''
    @@todo actually update view to expand to whole semester
    '''
    template_name = 'invcreate.html'
    model = HomeTable
    form_class = HomeTableForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        week = Term.get_current_week()
        start = week[0].strftime("%Y-%m-%d")
        end = week[4].strftime("%Y-%m-%d")
        return reverse_lazy('timetable:home_view', kwargs={'user_id':self.request.user.id, 'start':start, 'end':end})

    def get_context_data(self, **kwargs):
        semester = Term.get_current()
        week = semester.get_week()
        context = super(HomeRoomCreate, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(teacher=self.request.user, weekday__range=(week[0].strftime("%Y-%m-%d"), week[4].strftime("%Y-%m-%d")))
        if self.request.POST:
            context['timetables'] = HomeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = HomeTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = create_list_for_weeks()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.get_current() # todo
        week = semester.get_week()
        weeks = semester.get_count_of_weeks()
        #weeks = semester.end.isocalendar()[1] - semester.start.isocalendar()[1]
        formset = context['timetables']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.sememster = semester
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = week[i%5]
                instance.save()
                expand_to_term(instance, self.request.user, week[i%5], weeks) #@@todo
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class InvitedUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'inv/update.html'
    model = Invited
    form_class = InvitedTableForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(InvitedUpdate, self).get_context_data(**kwargs)
        qs = Invited.objects.filter(teacher=self.request.user, weekday__range=(self.kwargs['start'], self.kwargs['end']))
        if self.request.POST:
            context['timetables'] = InvitedTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = InvitedTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = create_list_for_weeks()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['timetables']
        if formset.is_valid():
            formset.save()
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))