from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SubjectTableForm
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

def subject_form(request):
    courses = []
    weekday = ['월', '화', '수', '목', '금']
    for row in range(8):
        for col in range(5):
            follow, is_follow = TimeTable.objects.get_or_create(teacher=request.user, weekday=weekday[col], time=row+1)
            if request.POST:
                form = SubjectTableForm(request.POST, initial={'id':follow.id, 'classNumber':follow.classNumber, 'time':follow.time, 'subject':follow.subject, 'weekday':follow.weekday })
                if form.is_valid():
                    follow.classNumber = request.POST['classNumber']
                    follow.subject = form.cleaned_data.get('subject')
                    follow.save()
                    redirect('timetable/subject_form.html')
                else:
                    print(form.errors)
            else:
                 form = SubjectTableForm(initial={'id':follow.id, 'classNumber':follow.classNumber, 'time':follow.time, 'subject':follow.subject, 'weekday':follow.weekday })
            courses.append(form)

    context = {
        'courses': courses,
        'weekday': weekday,
    }

    return render(request, 'timetable/subject_form.html', context )

def subject_view(request):
    week  = [[0]*5]*8
    weeks = ['월', '화', '수', '목', '금']
    for row in range(8):
        for col in range(5):
            form = TimeTable.objects.get(teacher=request.user, weekday=weeks[col], time=row+1)
            week[row][col] = form
            print(form)
    context = {
        'weekday':weeks,
        'week':week,
    }

    return render(request, 'timetable/subject_view.html', context )
