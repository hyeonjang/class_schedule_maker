from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView, WeekArchiveView
from django.utils import timezone
from django.contrib import messages

from school.models import Term, ClassRoom, Subject
from .forms import TimeTableForm, TimeTableViewForm 
from .forms import TimeTableCreateFormset, TimeTableUpdateFormset, TimeTableViewFormset
from .models import TimeTable
from .utils  import mon_to_fri, expand_inst_to_term

##########################################################
### Teacher Roles == Subject Features
class SubjectCreate(CreateView):
    template_name = 'SubjectCreate.html'
    model = TimeTable
    form_class = TimeTableForm

    def get_success_url(self):
        return redirect('sub_view') 

    def get_context_data(self, **kwargs):
        context= super(SubjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TimeTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['formset'] = TimeTableCreateFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.objects.get(pk=1)
        week = mon_to_fri(semester.start.year, semester.start.isocalendar()[1])
        weeks = semester.end.isocalendar()[1]-semester.start.isocalendar()[1]
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.semester = semester
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = week[i%5]
                instance.save()
                expand_inst_to_term(instance, week[i%5], weeks)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class SubjectUpdate(UpdateView):
    template_name = 'SubjectUpdate.html'
    model = TimeTable
    form_class = TimeTableForm
    success_url = '/'

    def get_object(self, queryset=None):
         return self.request.user

    def get_context_data(self, **kwargs):
        context = super(SubjectUpdate, self).get_context_data(**kwargs)
        qs = TimeTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04"))
        
        if self.request.is_ajax:
            startdate = self.request.GET.get('startdate')
            enddate = self.request.GET.get('enddate')
            if startdate and enddate:
                startdate = startdate[0:10] # iso format
                enddate = enddate[0:10]
                qs = TimeTable.objects.filter(teacher=self.request.user, weekday__range=(startdate, enddate))

        if self.request.POST:
            context['TimeTables'] = TimeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['TimeTables'] = TimeTableUpdateFormset(instance=self.request.user, queryset=qs)
        # print(context['TimeTables'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['TimeTables']
        if formset.is_valid():
            formset.save()
            messages.success(self.request, 'success', extra_tags='alert')
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, 'dd')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['TimeTables']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class SubjectView(TemplateView):
    template_name = 'SubjectView.html'
    model = TimeTable
    form_class = TimeTableViewForm

    def get_success_url(self):
        return redirect('sub_view') 

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['TimeTables'] = TimeTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04"))
        # print(context['TimeTables'])
        return context

### the end of subject
##########################################################

##########################################################
### instatiate HomeRoom TimeTable model for Semester in django admin

##########################################################
### Teacher Roles == Homeroom Features
class HomeRoomCreate(CreateView):
    template_name = 'HomeRoomCreate.html'
    model = TimeTable
    form_class = TimeTableForm

    def get_success_url(self):
        return redirect('sub_view') 

    def get_context_data(self, **kwargs):
        context= super(HomeRoomCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TimeTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['formset'] = TimeTableCreateFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        semester = Term.objects.get(pk=1)
        week = mon_to_fri(semester.start.year, semester.start.isocalendar()[1])
        weeks = semester.end.isocalendar()[1]-semester.start.isocalendar()[1]
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.semester = semester
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = week[i%5]
                instance.save()
                expand_inst_to_term(instance, week[i%5], weeks)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class HomeRoomUpdate(UpdateView):
    template_name = 'SubjectUpdate.html'
    model = TimeTable
    form_class = TimeTableForm
    success_url = '/'

    def get_object(self, queryset=None):
         return self.request.user

    def get_context_data(self, **kwargs):
        context = super(HomeRoomUpdate, self).get_context_data(**kwargs)
        qs = TimeTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04"))
        
        if self.request.is_ajax:
            startdate = self.request.GET.get('startdate')
            enddate = self.request.GET.get('enddate')
            if startdate and enddate:
                startdate = startdate[0:10] # iso format
                enddate = enddate[0:10]
                qs = TimeTable.objects.filter(teacher=self.request.user, weekday__range=(startdate, enddate))

        if self.request.POST:
            context['TimeTables'] = TimeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['TimeTables'] = TimeTableUpdateFormset(instance=self.request.user, queryset=qs)
        # print(context['TimeTables'])
        return context

class HomeRoomView(TemplateView):
    template_name = 'HomeRoomView.html'
    model = TimeTable
    form_class = TimeTableViewForm

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        context = super(HomeRoomView, self).get_context_data(**kwargs)
        classNum = self.request.user.get_classRoom()

        qs = TimeTable.objects.filter(classRoom=1, weekday__range=("2020-08-31", "2020-09-04"))
        context['TimeTables'] = TimeTableViewFormset(instance=self.request.user, queryset=qs)
        
        print(context['TimeTables'])
        return context