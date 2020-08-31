from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView, WeekArchiveView
from django.utils import timezone

from school.models import Term, ClassRoom, Subject
from .forms  import WeekSelectForm, TimeTableForm, TimeTableInlineFormset
from .models import TimeTable
from .utils  import monday_of_week

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
            context['form']    = WeekSelectForm(self.request.POST)
            context['formset'] = TimeTableInlineFormset(self.request.POST, instance=self.request.user)
        else:
            context['form']    = WeekSelectForm()
            context['formset'] = TimeTableInlineFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        weekform = context['form'].data['week']
        yw = (int(weekform[0:4]), int(weekform[6:8]))
        monday = monday_of_week(yw[0], yw[1])
        week = [monday, monday+timezone.timedelta(days=1), monday+timezone.timedelta(days=2), monday+timezone.timedelta(days=3), monday+timezone.timedelta(days=4) ]
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
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

class SubjectView(CreateView):
    template_name = 'SubjectView.html'
    model = TimeTable
    form_class = TimeTableForm

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        context= super(SubjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form']    = WeekSelectForm(self.request.POST)
            context['formset'] = TimeTableInlineFormset(self.request.POST, instance=self.request.user)
        else:
            context['form']    = WeekSelectForm()
            context['formset'] = TimeTableInlineFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        weekform = context['form'].data['week']
        yw = (int(weekform[0:4]), int(weekform[6:8]))
        monday = monday_of_week(yw[0], yw[1])
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = monday + timezone.timedelta(days=i)
                instance.save()
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

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        context= super(SubjectUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form']    = WeekSelectForm(self.request.POST)
            context['formset'] = TimeTableInlineFormset(self.request.POST, instance=self.request.user)
        else:
            context['form']    = WeekSelectForm()
            context['formset'] = TimeTableInlineFormset()
        return context

    # Validate forms
    def form_valid(self, form):
        context = self.get_context_data()
        weekform = context['form'].data['week']
        year = int(context['form'].data['week'][0:4])
        week = int(context['form'].data['week'][6:8])
        monday = monday_of_week(year, week)
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = monday + timezone.timedelta(days=i)
                instance.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

class HomeRoomCreate(CreateView):
    template_name = 'SubjectCreate.html'
    model = TimeTable
    form_class = TimeTableForm

    def get_success_url(self):
        return redirect('view') 

    def get_context_data(self, **kwargs):
        context= super(HomeRoomCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form']    = WeekSelectForm(self.request.POST)
            context['formset'] = TimeTableInlineFormset(self.request.POST, instance=self.request.user)
        else:
            context['form']    = WeekSelectForm()
            context['formset'] = TimeTableInlineFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        weekform = context['form'].data['week']
        yw = (int(weekform[0:4]), int(weekform[6:8]))
        monday = monday_of_week(yw[0], yw[1])
        formset = context['formset']
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = monday + timezone.timedelta(days=i)
                instance.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

# Subject role Teacher view
# class SubjectView(WeekArchiveView):
#     template_name = 'SubjectView.html'
#     queryset = TimeTable.objects.all()
#     date_field = "weekday"
#     week_format = "%W"
#     allow_future = True
