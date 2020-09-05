from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .models import Holiday, ClassRoom, Subject
from .forms import GradeFilterForm, TermModelForm, HolidayModelForm, ClassRoomModelForm, SubjectModelForm
from .utils import expand_inst_to_term

class SchoolManageListView(generic.ListView):
    context_object_name = 'subjects'
    template_name = 'manage_school.html'
    form_class = TermModelForm

    def get_queryset(self):
        return Subject.objects.order_by('grade')
    
    def get_context_data(self, **kwargs):
        context = super(SchoolManageListView, self).get_context_data()
        qs_h = Holiday.objects.all()
        qs_c = ClassRoom.objects.all()
        qs_s = Subject.objects.all()
        if 'grade' in self.request.GET:
            qs_c = ClassRoom.objects.filter(grade=int(self.request.GET['grade']))
            qs_s = Subject.objects.filter(grade=int(self.request.GET['grade']))
       
        context.update({
            'holidays' : qs_h,
            'classrooms' : qs_c,
            'subjects' : qs_s,
            'form' : self.form_class,
        })
       
        return context
    
    def form_valid(self, form):
        return reverse_lazy('index')

class GradeFilterView(BSModalFormView):
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
        return reverse_lazy('manage_school') + self.filter

########################################################
### Holiday Features

class HolidayCreateView(BSModalCreateView):
    template_name = "holiday/create.html"
    form_class = HolidayModelForm
    success_message = 'Success: Holiday was added.'
    success_url = reverse_lazy('manage_school')

class HolidayUpdateView(BSModalUpdateView):
    model = Holiday
    template_name = 'holiday/update.html'
    form_class = HolidayModelForm
    success_message = 'Success: Holiday was updated.'
    success_url = reverse_lazy('manage_school')

class HolidayDeleteView(BSModalDeleteView):
    model = Holiday
    template_name = 'holiday/delete.html'
    success_message = 'Success: Holiday was deleted.'
    success_url = reverse_lazy('manage_school')

### the end of subject feautures
########################################################
### ClassRoom Features

class ClassRoomCreateView(BSModalCreateView):
    template_name = "classroom/create.html"
    form_class = ClassRoomModelForm
    success_message = 'Success: Subject was created.'
    success_url = reverse_lazy('manage_school')

class ClassRoomUpdateView(BSModalUpdateView):
    model = ClassRoom
    template_name = 'classroom/update.html'
    form_class = ClassRoomModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('manage_school')

class ClassRoomDeleteView(BSModalDeleteView):
    model = ClassRoom
    template_name = 'classroom/delete.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('manage_school')

def classrooms(request):
    data = dict()
    if request.method == 'GET':
        classrooms = ClassRoom.objects.all()
        data['table'] = render_to_string(
            'classroom/_table.html',
            {'classrooms': classrooms},
            request=request
        )
        return JsonResponse(data)

### the end of classroom feautures
########################################################
### Subject Features

class SubjectCreateView(BSModalCreateView):
    template_name = "subject/create.html"
    form_class = SubjectModelForm
    success_message = 'Success: Subject was created.'
    success_url = reverse_lazy('manage_school')

class SubjectUpdateView(BSModalUpdateView):
    model = Subject
    template_name = 'subject/update.html'
    form_class = SubjectModelForm
    success_message = 'Success: Subject was updated.'
    success_url = reverse_lazy('manage_school')

class SubjectDeleteView(BSModalDeleteView):
    model = Subject
    template_name = 'subject/delete.html'
    success_message = 'Success: Subject was deleted.'
    success_url = reverse_lazy('manage_school')

### the end of subject feautures
########################################################
