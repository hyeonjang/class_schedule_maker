from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SubjectTableForm
from .models import TimeTable

def home(request):
    if request.user is None:
        return render(request, 'accounts/login.html')
    else:
        return render(request, 'timetable/subject_view.html')

def classroom(request):
    if request.POST:
        form = TableForm(request.POST)
        return redirect('accounts/login.html')
    else:
        form = TableForm()
    return render(request, 'timetable/classroom.html', {'form': form} )

def subject_form(request):
    weekday = ['월', '화', '수', '목', '금']
    week = [[0]*5]*8
    for row in range(8):
        for col in range(5):
            follow, is_follow = TimeTable.objects.get_or_create(c_teacher=request.user, c_weekday=weekday[col], i_time=row+1)
            if request.POST:
                form = SubjectTableForm(request.POST)
                if form.is_valid() and form.has_changed():
                    follow.save()
                else:
                    print(form.errors)
            else:
                form = SubjectTableForm(initial={'classNumber':follow.classNumber, 'subject':follow.c_subject, 'weekday':follow.c_weekday })
            week[row][col] = form

    context = {
        'weekday':weekday,
        'week':week,
    }

    return render(request, 'timetable/subject_form.html', context )

def subject_view(request):
    weekday = ['월', '화', '수', '목', '금']
    week = [[0]*5]*8
    for row in range(8):
        for col in range(5):
            form = TimeTable.objects.get(c_teacher=request.user.id, c_weekday=weekday[col], i_time=row+1)
            week[row][col] = form
    return render(request, 'timetable/subject_view.html', {'week': week } )
