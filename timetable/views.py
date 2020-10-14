"""
module doc
"""
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalFormView
from school.models import Term, Subject, ClassRoom
from .models import SubjectTable, HomeTable, Invited
from .forms import TableCreateForm
from .forms import (SubjectTableForm, HomeTableForm, InvitedTableForm, SubjectTableUpdateFormset, HomeTableUpdateFormset, InvitedTableUpdateFormset)
from .utils import create_list_for_weeks
##########################################################
### Teacher Roles == Subject Features
class SubjectCreate(LoginRequiredMixin, BSModalFormView):
    '''
    class doc
    '''
    form_class = TableCreateForm
    template_name = 'create.html'

    def form_valid(self, form):
        if self.request.is_ajax(): #bug django-bootstrap-modal-forms twice redirection
            semester = form.cleaned_data['semester']
            week = semester.get_week()
            weeks = semester.get_count_of_weeks()
            bulk_tables = []
            for i in range(0, weeks+1):
                for j in range(0, 40):
                    new_table = SubjectTable(teacher=self.request.user, semester=semester, day=week[j%5] + timezone.timedelta(days=7*i), time=(j//5)%8+1)
                    bulk_tables.append(new_table)
            SubjectTable.objects.bulk_create(bulk_tables)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:sub_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

class SubjectUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'sub/update.html'
    model = SubjectTable
    form_class = SubjectTableForm

    # added member
    list_weeks = create_list_for_weeks()
    #semester = Term.objects.first()

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('timetable:sub_view', kwargs={'user_id':self.request.user.id, 'start':self.kwargs['start'], 'end':self.kwargs['end']})

    def get_context_data(self, **kwargs):
        context = super(SubjectUpdate, self).get_context_data(**kwargs)
        qs = SubjectTable.objects.filter(teacher=self.request.user, day__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "day")
        if self.request.POST:
            context['timetables'] = SubjectTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = SubjectTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = create_list_for_weeks()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['timetables']
        if formset.is_valid():
            weeks = []
            for week in self.list_weeks:
                if self.request.POST.get(f"{week[0].strftime('%W')}week") is not None:
                    weeks.append(self.request.POST.get(f"{week[0].strftime('%W')}week"))
            for form in formset:
                inst = form.save(commit=False)
                qs = SubjectTable.objects.filter(semester=Term.get_current(), teacher=self.request.user, day__iso_week_day=inst.day.isoweekday(), day__week__in=weeks, time=inst.time)
                for ins in qs:
                    ins.subject = inst.subject
                    ins.classroom = inst.classroom
                    ins.save()       
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class SubjectView(LoginRequiredMixin, generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'sub/view.html'
    model = SubjectTable

    def create_information(self):
        '''
        Return TimeTable information to Templates
        '''
        information = dict()
        semester = semester = Term.objects.first()
        classrooms = SubjectTable.objects.exclude(classroom=None).distinct('classroom').values_list('classroom', flat=True)

        for classroom in classrooms:
            weeks = semester.get_weeks_start_end()
            count_per_week = []
            for week in weeks:
                count_per_week.append(SubjectTable.objects.filter(teacher=self.request.user, classroom=classroom, day__range=(week[0].strftime("%Y-%m-%d"), week[1].strftime("%Y-%m-%d"))).count())
            dic = {ClassRoom.objects.get(pk=classroom):[count_per_week, SubjectTable.objects.filter(teacher=self.request.user, classroom=classroom).count()]}

            information.update(dic)
        return information

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:sub_view')

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['timetables'] = SubjectTable.objects.filter(semester=Term.get_current(), teacher=self.request.user, day__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "day")
        context['list_weeks'] = create_list_for_weeks()
        context['information'] = self.create_information()
        return context

class SubjectReset(LoginRequiredMixin, BSModalFormView):
    form_class = TableCreateForm
    template_name = 'reset.html'

    def form_valid(self, form):
        if self.request.is_ajax(): #bug django-bootstrap-modal-forms twice redirection
            semester = form.cleaned_data['semester']
            sub = SubjectTable.objects.filter(teacher=self.request.user, semester=semester)
            HomeTable.objects.filter(sub_teacher__in=sub).update(subject=None, sub_teacher=None)
            sub.update(classroom=None, subject=None)
        return redirect(self.get_success_url())

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:sub_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

### the end of subject
##########################################################
### Teacher Roles == Homeroom Features
class HomeroomCreate(LoginRequiredMixin, BSModalFormView):
    form_class = TableCreateForm
    template_name = 'create.html'

    def form_valid(self, form):
        if self.request.is_ajax(): #bug django-bootstrap-modal-forms twice redirection
            semester = form.cleaned_data['semester']
            week = semester.get_week()
            weeks = semester.get_count_of_weeks()
            bulk_tables = []
            for i in range(0, weeks+1):
                for j in range(0, 40):
                    classroom = self.request.user.return_by_type().classroom
                    new_table = HomeTable(teacher=self.request.user, classroom=classroom, semester=semester, day=week[j%5]+timezone.timedelta(days=7*i), time=(j//5)%8+1)
                    bulk_tables.append(new_table)
            HomeTable.objects.bulk_create(bulk_tables)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:home_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

class HomeroomUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'home/update.html'
    model = HomeTable
    form_class = HomeTableForm
    success_url = '/'

    list_weeks = create_list_for_weeks()
    #semester = Term.get_current()

    def auto_created_subject(self):
        from operator import itemgetter
        # picking algorithm
        sub_lis = []
        subjects = Subject.objects.filter(grade=self.request.user.return_by_type().get_grade())
        for subject in subjects:
            cur = HomeTable.objects.filter(subject=subject).count()
            tot = subject.count
            # caculate key value
            key = cur/tot
            sub_lis.append((key, subject))
        sub_lis = sorted(sub_lis, key=itemgetter(0))
        return sub_lis[0][1]

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(HomeroomUpdate, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(semester=self.semester, teacher=self.request.user, day__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "day")
        if self.request.POST:
            context['timetables'] = HomeTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = HomeTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = self.list_weeks
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['timetables']
        if formset.is_valid():
            weeks = []
            for week in self.list_weeks:
                # 0. query the being updated weeks
                if self.request.POST.get(f"{week[0].strftime('%W')}week") is not None:
                    weeks.append(self.request.POST.get(f"{week[0].strftime('%W')}week"))
            for form in formset:
                instance = form.save(commit=False)
                # 1. using django ORM
                qs = HomeTable.objects.filter(semester=Term.get_current(), teacher=self.request.user, day__iso_week_day=instance.day.isoweekday(), day__week__in=weeks, time=instance.time)
                # 2. excepting which has sub_teahcer or inv_teacher
                query = qs.filter(sub_teacher=None)&qs.filter(inv_teacher=None)
                # 3. update subject
                if form.cleaned_data['auto']:
                    query.update(subject=self.auto_created_subject())
                else:
                    query.update(subject=instance.subject)
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class HomeroomReset(LoginRequiredMixin, BSModalFormView):
    '''
    Table reset view
    '''
    form_class = TableCreateForm
    template_name = 'reset.html'

    def form_valid(self, form):
        if self.request.is_ajax(): #bug django-bootstrap-modal-forms twice redirection
            semester = form.cleaned_data['semester']
            HomeTable.objects.filter(teacher=self.request.user, semester=semester, sub_teacher=None, inv_teacher=None).update(subject=None)
        return redirect(self.get_success_url())

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:home_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

class HomeroomView(LoginRequiredMixin, generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'home/view.html'
    model = HomeTable

    def create_information(self):
        '''
        Return TimeTable information to Templates
        '''
        information = dict()
        teacher = self.request.user.return_by_type()
        #semester = Term.get_current()
        subjects = Subject.objects.filter(grade=teacher.get_grade())

        for subject in subjects:
            weeks = semester.get_weeks_start_end()
            count_per_week = []
            for week in weeks:
                count_per_week.append(HomeTable.objects.filter(teacher=self.request.user, subject=subject, day__range=(week[0].strftime("%Y-%m-%d"), week[1].strftime("%Y-%m-%d"))).count())
            dic = {subject:[count_per_week, HomeTable.objects.filter(teacher=self.request.user, subject=subject).count(), subject.count]}

            information.update(dic)
        return information

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:home_view')

    def get_context_data(self, **kwargs):
        context = super(HomeroomView, self).get_context_data(**kwargs)
        qs = HomeTable.objects.filter(semester=Term.get_current(), teacher=self.request.user, day__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "day")
        context['timetables'] = qs
        context['list_weeks'] = create_list_for_weeks()
        context['information'] = self.create_information()
        return context

### the end of homeroom
##########################################################
### Teacher Roles == Invited
class InvitedCreate(LoginRequiredMixin, BSModalFormView):
    '''
    class doc
    '''
    form_class = TableCreateForm
    template_name = 'create.html'

    def form_valid(self, form):
        if self.request.is_ajax(): #bug django-bootstrap-modal-forms twice redirection
            semester = form.cleaned_data['semester']
            user = self.request.user.return_by_type()
            print(self.request.user)
            week = semester.get_week(user.start)
            weeks = semester.get_count_of_weeks(user.start, user.end)
            bulk_tables = []
            for i in range(0, weeks+1):
                for j in range(0, 40):
                    new_table = Invited(teacher=self.request.user, semester=semester, day=week[j%5] + timezone.timedelta(days=7*i), time=(j//5)%8+1)
                    bulk_tables.append(new_table)
            Invited.objects.bulk_create(bulk_tables)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:inv_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

class InvitedUpdate(LoginRequiredMixin, generic.UpdateView):
    '''
    class doc
    '''
    template_name = 'inv/update.html'
    model = Invited
    form_class = InvitedTableForm

    # added member
    list_weeks = create_list_for_weeks()
    #semester = Term.get_current()

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:inv_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

    def get_context_data(self, **kwargs):
        context = super(InvitedUpdate, self).get_context_data(**kwargs)
        qs = Invited.objects.filter(teacher=self.request.user, day__range=(self.kwargs['start'], self.kwargs['end']))
        if self.request.POST:
            context['timetables'] = InvitedTableUpdateFormset(self.request.POST, instance=self.request.user, queryset=qs)
        else:
            context['timetables'] = InvitedTableUpdateFormset(instance=self.request.user, queryset=qs)
        context['list_weeks'] = self.list_weeks
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['timetables']
        if formset.is_valid():
            weeks = []
            for week in self.list_weeks:
                if self.request.POST.get(f"{week[0].strftime('%W')}week") is not None:
                    weeks.append(self.request.POST.get(f"{week[0].strftime('%W')}week"))
            for form in formset:
                inst = form.save(commit=False)
                qs = Invited.objects.filter(semester=self.semester, teacher=self.request.user, day__iso_week_day=inst.day.isoweekday(), day__week__in=weeks, time=inst.time)
                for ins in qs:
                    ins.subject = inst.subject
                    ins.classroom = inst.classroom
                    ins.save() 
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class InvitedReset(LoginRequiredMixin, BSModalFormView):
    '''
    Table reset view
    '''
    form_class = TableCreateForm
    template_name = 'reset.html'

    def form_valid(self, form):
        if self.request.is_ajax(): #bug django-bootstrap-modal-forms twice redirection
            semester = form.cleaned_data['semester']
            Invited.objects.filter(teacher=self.request.user, semester=semester).update(subject=None)
        return redirect(self.get_success_url())

    def get_success_url(self):
        week = Term.get_current_week()
        return reverse_lazy('timetable:inv_view', kwargs={'user_id':self.request.user.id, 'start':week[0], 'end':week[4]})

class InvitedView(generic.TemplateView):
    '''
    class doc
    '''
    template_name = 'inv/view.html'
    model = HomeTable

    def create_information(self):
        '''
        Return TimeTable information to Templates
        '''
        information = dict()
        semester = Term.get_current()
        classrooms = Invited.objects.exclude(classroom=None).distinct('classroom').values_list('classroom', flat=True)

        for classroom in classrooms:
            weeks = semester.get_weeks_start_end()
            count_per_week = []
            for week in weeks:
                count_per_week.append(Invited.objects.filter(teacher=self.request.user, classroom=classroom, day__range=(week[0].strftime("%Y-%m-%d"), week[1].strftime("%Y-%m-%d"))).count())
            dic = {ClassRoom.objects.get(pk=classroom):[count_per_week, Invited.objects.filter(teacher=self.request.user, classroom=classroom).count()]}

            information.update(dic)
        return information

    def get_success_url(self):
        '''
        class doc
        '''
        return redirect('timetable:inv_view')
    def get_context_data(self, **kwargs):
        context = super(InvitedView, self).get_context_data(**kwargs)
        qs = Invited.objects.filter(teacher=self.request.user, day__range=(self.kwargs['start'], self.kwargs['end'])).order_by("time", "day")
        context['timetables'] = qs
        context['list_weeks'] = create_list_for_weeks()
        context['information'] = self.create_information()
        return context
