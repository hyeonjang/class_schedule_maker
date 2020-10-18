'''
module doc
'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.generic import (
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView
)
from .models import Term, Holiday, ClassRoom, Subject
from .forms import (
    SchoolModelForm,
    GradeFilterForm,
    TermModelForm,
    HolidayModelForm,
    ClassRoomModelForm,
    SubjectModelForm,
    )

########################################################
### management views
class SchoolSignUp(BSModalCreateView):
    '''
    inherited
    '''
    form_class = SchoolModelForm
    template_name = 'school/create.html'
    success_url = reverse_lazy('account:login')

class TermManageListView(LoginRequiredMixin, generic.ListView):
    '''
    module doc
    '''
    context_object_name = 'subjects'
    template_name = 'manage_semester.html'

    def get_queryset(self):
        return Term.objects.order_by()

    def get_context_data(self, **kwargs):
        context = super(TermManageListView, self).get_context_data()
        qs_t = Term.objects.filter(school=self.request.user.school)
        qs_h = Holiday.objects.filter(school=self.request.user.school)
        context.update({
            'semesters' : qs_t,
            'holidays' : qs_h,
        })
        return context

class SubjectManageListView(LoginRequiredMixin, generic.ListView):
    '''
    module doc
    '''
    context_object_name = 'subjects'
    template_name = 'manage_subject.html'

    def get_queryset(self):
        return Subject.objects.order_by('grade')

    def get_context_data(self, **kwargs):
        context = super(SubjectManageListView, self).get_context_data()
        qs_s = Subject.objects.filter(school=self.request.user.school)
        if 'grade' in self.request.GET:
            qs_s = qs_s.filter(grade=int(self.request.GET['grade']))
        context.update({
            'subjects' : qs_s,
        })
        return context

class ClassRoomManageListView(LoginRequiredMixin, generic.ListView):
    '''
    module doc
    '''
    context_object_name = 'subjects'
    template_name = 'manage_classroom.html'

    def get_queryset(self):
        return ClassRoom.objects.order_by('grade')

    def get_context_data(self, **kwargs):
        context = super(ClassRoomManageListView, self).get_context_data()
        qs_c = ClassRoom.objects.filter(school=self.request.user.school)
        if 'grade' in self.request.GET:
            qs_c = qs_c.filter(grade=int(self.request.GET['grade']))
        context.update({
            'classrooms' : qs_c,
        })
        return context

class ClassRoomGradeFilterView(BSModalFormView):
    '''
    module doc
    '''
    template_name = 'classroom/filter.html'
    form_class = GradeFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?grade=' + form.cleaned_data['grade']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('school:manage_classroom') + self.filter

class SubjectGradeFilterView(BSModalFormView):
    '''
    module doc
    '''
    template_name = 'subject/filter.html'
    form_class = GradeFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?grade=' + form.cleaned_data['grade']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('school:manage_subject') + self.filter

### the end of management feautures
########################################################
########################################################
### Holiday Features

class SemesterCreateView(BSModalCreateView):
    '''
    module doc
    '''
    template_name = "semester/create.html"
    form_class = TermModelForm
    success_message = 'Success: Semester was added.'

    def get_success_url(self):
        return reverse_lazy('school:manage_semester', kwargs={'school_id':self.request.user.school.pk})

    def form_valid(self, form):
        if self.request.is_ajax():
            instance = form.save(commit=False)
            instance.school = self.request.user.school
            instance.save()
        return redirect(self.get_success_url())

class SemesterUpdateView(BSModalUpdateView):
    '''
    module doc
    '''
    model = Term
    template_name = 'semester/update.html'
    form_class = TermModelForm

    def get_success_url(self):
        return reverse_lazy('school:manage_semester', kwargs={'school_id':self.request.user.school.pk})

class SemesterDeleteView(BSModalDeleteView):
    '''
    module doc
    '''
    model = Term
    template_name = 'semester/delete.html'
    success_message = 'Success: Semester was deleted.'

    def get_success_url(self):
        return reverse_lazy('school:manage_semester', kwargs={'school_id':self.request.user.school.pk})

def semesters(request):
    '''
    module doc
    '''
    data = dict()
    if request.method == 'GET':
        term = Term.objects.filter(school=request.user.school.pk)
        data['table'] = render_to_string(
            'semester/_table.html',
            {'semesters': term},
            request=request
        )
        return JsonResponse(data)

### the end of subject feautures
########################################################
########################################################
### Holiday Features

class HolidayCreateView(BSModalCreateView):
    '''
    module doc
    '''
    template_name = "holiday/create.html"
    form_class = HolidayModelForm
    success_message = 'Success: Holiday was added.'

    def get_success_url(self):
        return reverse_lazy('school:manage_semester', kwargs={'school_id':self.request.user.school.pk})

    def form_valid(self, form):
        if self.request.is_ajax():
            instance = form.save(commit=False)
            instance.school = self.request.user.school
            instance.save()
        return redirect(self.get_success_url())

class HolidayUpdateView(BSModalUpdateView):
    '''
    module doc
    '''
    model = Holiday
    template_name = 'holiday/update.html'
    form_class = HolidayModelForm
    success_message = 'Success: Holiday was deleted.'

    def get_success_url(self):
        return reverse_lazy('school:manage_semester', kwargs={'school_id':self.request.user.school.pk})

class HolidayDeleteView(BSModalDeleteView):
    '''
    module doc
    '''
    model = Holiday
    template_name = 'holiday/delete.html'
    success_message = 'Success: Holiday was deleted.'

    def get_success_url(self):
        return reverse_lazy('school:manage_semester', kwargs={'school_id':self.request.user.school.pk})

def holidays(request):
    '''
    module doc
    '''
    data = dict()
    if request.method == 'GET':
        holidays = Holiday.objects.filter(school=request.user.school)
        data['table'] = render_to_string(
            'holiday/_table.html',
            {'holidays': holidays},
            request=request
        )
        return JsonResponse(data)

### the end of subject feautures
########################################################
### ClassRoom Features

class ClassRoomCreateView(BSModalCreateView):
    '''
    module doc
    '''
    template_name = "classroom/create.html"
    form_class = ClassRoomModelForm

    def get_success_url(self):
        return reverse_lazy('school:manage_classroom', kwargs={'school_id':self.request.user.school.pk})

class ClassRoomUpdateView(BSModalUpdateView):
    '''
    module doc
    '''
    model = ClassRoom
    template_name = 'classroom/update.html'
    form_class = ClassRoomModelForm

    def get_success_url(self):
        return reverse_lazy('school:manage_classroom', kwargs={'school_id':self.request.user.school.pk})

class ClassRoomDeleteView(BSModalDeleteView):
    '''
    module doc
    '''
    model = ClassRoom
    template_name = 'classroom/delete.html'
    success_message = 'Success: Book was deleted.'

    def get_success_url(self):
        return reverse_lazy('school:manage_classroom', kwargs={'school_id':self.request.user.school.pk})

def classrooms(request):
    '''
    module doc
    '''
    data = dict()
    if request.method == 'GET':
        clss = ClassRoom.objects.filter(school=request.user.school)
        data['table'] = render_to_string(
            'classroom/_table.html',
            {'classrooms': clss},
            request=request
        )
        return JsonResponse(data)

### the end of classroom feautures
########################################################
### Subject Features

class SubjectCreateView(BSModalCreateView):
    '''
    module doc
    '''
    template_name = "subject/create.html"
    form_class = SubjectModelForm

    def get_success_url(self):
        return reverse_lazy('school:manage_subject', kwargs={'school_id':self.request.user.school.pk})

class SubjectUpdateView(BSModalUpdateView):
    '''
    module doc
    '''
    model = Subject
    template_name = 'subject/update.html'
    form_class = SubjectModelForm
    form_class = SubjectModelForm

    def get_success_url(self):
        return reverse_lazy('school:manage_subject', kwargs={'school_id':self.request.user.school.pk})

class SubjectDeleteView(BSModalDeleteView):
    '''
    module doc
    '''
    model = Subject
    template_name = 'subject/delete.html'
    success_message = 'Success: Subject was deleted.'

    def get_success_url(self):
        return reverse_lazy('school:manage_subject', kwargs={'school_id':self.request.user.school.pk})

def subjects(request):
    '''
    module doc
    '''
    data = dict()
    if request.method == 'GET':
        subjects = Subject.objects.filter(school=request.user.school)
        data['table'] = render_to_string(
            'subject/_table.html',
            {'subjects': subjects},
            request=request
        )
        return JsonResponse(data)
### the end of subject feautures
########################################################
