from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .forms import SubjectTableForm, TableForm
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
    courses = []
    weekday = ['월', '화', '수', '목', '금']
    for row in range(8):
        for col in range(5):
            if request.POST:
                form = TableForm(request.POST)
                if form.is_valid():
                    course = form.save(commit=False)
                    course.teacher = request.user
                    course.time = row+1
                    course.weekday = weekday[col]
                    course.classNumber = 0
                    course.save()
                else:
                    print(form.errors)
            else:
                 form = TableForm()
            courses.append(form)

    context = {
        'courses': courses,
        'weekday': weekday,
    }

    return render(request, 'timetable/create.html', context )

def modify(request):
    courses = []
    weekday = ['월', '화', '수', '목', '금']
    forms = []
    for row in range(8):
        for col in range(5):
            follow = TimeTable.objects.get(teacher=request.user, weekday=weekday[col], time=row+1)
            if request.POST:
                form = TableForm(request.POST, instance=follow)
                if form.is_valid():
                    with transaction.atomic(): 
                        form.save()
                else:
                    from django.contrib import messages
                    messages.error(request, form.errors)
            else:
                print("get")
                form = TableForm(instance=follow, initial={'id':follow.id})
            courses.append(form)

    context = {
        'courses': courses,
        'weekday': weekday,
    }

    for f in forms:
        f.save()

    return render(request, 'timetable/modify.html', context )

def subject_view(request):
    courses = []
    weekday = ['월', '화', '수', '목', '금']
    for row in range(8):
        for col in range(5):
            form = TimeTable.objects.get(teacher=request.user, weekday=weekday[col], time=row+1)
            courses.append(form)
    context = {
        'courses': courses,
        'weekday': weekday,
    }
    return render(request, 'timetable/subject_view.html', context )
