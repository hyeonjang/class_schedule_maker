from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from .forms import TableForm
from .models import TimeTable

def home(request):
    if request.user is None:
        return render(request, 'accounts/login.html')
    else:
        return subject_view(request)

def classroom(request):
    if request.POST:
        form = TableForm(request.POST)
        return redirect('accounts/login.html')
    else:
        form = TableForm()
    return render(request, 'timetable/classroom.html', {'form': form} )

def create(request):
    weekday = ['월', '화', '수', '목', '금']
    TimeTableSet = inlineformset_factory(User, TimeTable, extra=40, form=TableForm)
    teacher = request.user
    if request.POST:
        formset = TimeTableSet(request.POST, instance=teacher)
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = form.save(commit=False)
                instance.time = (i//5)%8+1 # row major table input
                instance.weekday = weekday[i%5]
                instance.save()
        else:
            print(formset.errors)
        return redirect('view') 
    else:
        formset = TimeTableSet()

    context = {
        'formset': formset,
        'weekday': weekday,
    }

    return render(request, 'timetable/create.html', context)

def modify(request):
    weekday = ['월', '화', '수', '목', '금']
    TimeTableSet = inlineformset_factory(User, TimeTable, extra=40, form=TableForm)
    teacher = request.user
    if request.POST:
        formset = TimeTableSet(request.POST, instance=teacher)
        if formset.is_valid():
            for i, form in enumerate(formset):
                instance = TimeTable.objects.get(teacher=request.user, time=(i//5)%8+1, weekday=weekday[i%5])
                instance.classRoom = form.cleaned_data.get('classRoom')
                instance.subject = form.cleaned_data.get('subject')
                instance.save()
        else:
            print(formset.errors)
        return redirect('view') 
    else:
        formset = TimeTableSet()

    context = {
        'formset': formset,
        'weekday': weekday,
    }

    return render(request, 'timetable/modify.html', context )

def subject_view(request):
    formset = []
    weekday = ['월', '화', '수', '목', '금']
    for row in range(8):
        for col in range(5):
            form = TimeTable.objects.get(teacher=request.user, weekday=weekday[col], time=row+1)
            formset.append(form)
    context = {
        'formset': formset,
        'weekday': weekday,
    }
    return render(request, 'timetable/subject_view.html', context )
