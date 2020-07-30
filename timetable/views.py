from django.shortcuts import render
from django.utils import timezone
from .models import TimeTable

def table_list(request):
    tables = TimeTable.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'timetable/table_list.html', {'tables': tables})