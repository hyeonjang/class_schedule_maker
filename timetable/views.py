from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import TableForm

def classroom(request):
    if request.POST:
        form = TableForm(request.POST)
        return redirect('accounts/login.html')
    else:
        form = TableForm()
    return render(request, 'timetable/classroom.html', {'form': form})

# @@todo 2-array;
def subject(request):
    l_form = [[]]
    for i in range(0,5):
        for j in range(0,6):
            form = TableForm(request.POST)
        l_form.append(form)
    return render(request, 'timetable/subject.html', {'form': l_form})