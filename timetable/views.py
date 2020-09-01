from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView, WeekArchiveView
from django.utils import timezone
import json

from school.models import Term, ClassRoom, Subject
from .forms import WeekSelectForm, TermSelectForm, TimeTableForm 
from .forms import TimeTableCreateFormset, TimeTableUpdateFormset
from .models import TimeTable
from .utils  import mon_to_fri, expand_inst_to_term

def home(request):
    if request.user is None:
        return render(request, 'accounts/login.html')
    else:
        return redirect('view', request.user)

class SubjectCreate(CreateView):
    template_name = 'SubjectCreate.html'
    model = TimeTable
    form_class = TimeTableForm

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        context= super(SubjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['select'] = TermSelectForm(self.request.POST)
            context['formset'] = TimeTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['select'] = TermSelectForm()
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

    def get_object(self, queryset=None):
         return self.request.user

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        week = self.request.GET.get('date')
        context = super(SubjectUpdate, self).get_context_data(**kwargs)
        qs = TimeTable.objects.filter(teacher=self.request.user, weekday__range=("2020-08-31", "2020-09-04"))
        if self.request.POST:
            context['select'] = WeekSelectForm(self.request.POST)
            context['formset'] = TimeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['select'] = WeekSelectForm()
            context['formset'] = TimeTableUpdateFormset(instance=self.request.user, queryset=qs)
        return context
    
    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class SubjectView(TemplateView):
    template_name = 'SubjectView.html'
    model = TimeTable
    form_class = TimeTableForm

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TimeTableCreateFormset(self.request.POST, instance=self.request.user)
        else:
            context['formset'] = TimeTableCreateFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        weekform = context['form'].data['week']
        yw = (int(weekform[0:4]), int(weekform[6:8]))
        monday = mon_to_fri(yw[0], yw[1])
        formset = context['formset']
        for i, form in enumerate(formset):
            instance = form.save(commit=False)
            instance.semester = formset[0].semester
            instance.time = (i//5)%8+1 # row major table input
            instance.weekday = monday + timezone.timedelta(days=i)
            instance.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))
# class HomeRoomCreate(CreateView):
#     template_name = 'SubjectCreate.html'
#     model = TimeTable
#     form_class = TimeTableForm

#     def get_success_url(self):
#         return redirect('view') 

#     def get_context_data(self, **kwargs):
#         context= super(HomeRoomCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['form']    = TermSelectForm(self.request.POST)
#             context['formset'] = TimeTableInlineFormset(self.request.POST, instance=self.request.user)
#         else:
#             context['form']    = TermSelectForm()
#             context['formset'] = TimeTableInlineFormset()
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         weekform = context['form'].data['week']
#         yw = (int(weekform[0:4]), int(weekform[6:8]))
#         monday = mon_to_fri(yw[0], yw[1])
#         formset = context['formset']
#         if formset.is_valid():
#             for i, form in enumerate(formset):
#                 instance = form.save(commit=False)
#                 instance.time = (i//5)%8+1 # row major table input
#                 instance.weekday = monday + timezone.timedelta(days=i)
#                 instance.save()
#             return redirect(self.get_success_url())
#         else:
#             return self.render_to_response(self.get_context_data(form=form))

#     def form_invalid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']
#         print(formset.errors)
#         return self.render_to_response(self.get_context_data(form=form))

# Subject role Teacher view
# class SubjectView(WeekArchiveView):
#     template_name = 'SubjectView.html'
#     queryset = TimeTable.objects.all()
#     date_field = "weekday"
#     week_format = "%W"
#     allow_future = True
