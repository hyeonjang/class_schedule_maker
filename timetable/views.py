from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import TableForm

def table_list(request):
    if request.POST:
        form = TableForm(request.POST)
        return redirect('accounts/login.html')
    else:
        form = TableForm()
    return render(request, 'timetable/timetable.html', {'form': form})