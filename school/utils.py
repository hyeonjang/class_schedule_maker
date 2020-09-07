import time
from django.utils import timezone

from timetable.models import TimeTable
from .models import Term

def mon_to_fri(year, week):
    """
    Returns a datetime for the monday of the given week of the given year.
    """
    str_time = time.strptime('{0} {1} 1'.format(year, week), '%Y %W %w')
    date = timezone.datetime(year=str_time.tm_year, month=str_time.tm_mon,
                             day=str_time.tm_mday, tzinfo=timezone.utc)
    if timezone.datetime(year, 1, 4).isoweekday() > 4:
        # ISO 8601 where week 1 is the first week that has at least 4 days in
        # the current year
        date -= timezone.timedelta(days=7)
    return [ date, 
            date+timezone.timedelta(days=1), 
            date+timezone.timedelta(days=2), 
            date+timezone.timedelta(days=3), 
            date+timezone.timedelta(days=4)]

def expand_inst_to_term(instance, day, iter):
    for i in range(1, iter):
        copy = instance
        copy.pk = None
        copy.weekday = day+timezone.timedelta(days=7*i)
        copy.save()


def instantiate_classroom_timetable(semester, classRoom):
    week = mon_to_fri(semester.start.year, semester.start.isocalendar()[1])
    weeks = semester.end.isocalendar()[1]-semester.start.isocalendar()[1]
    
    for i in range(0, 40):
        instance, is_follow = TimeTable.objects.get_or_create(
            classRoom = classRoom, 
            semester = semester, 
            weekday = week[i%5],
            time = (i//5)%8+1
            )
        expand_inst_to_term(instance, week[i%5], weeks)

def instantiate_teacher_timetable(semester, teacher):
    week = mon_to_fri(semester.start.year, semester.start.isocalendar()[1])
    weeks = semester.end.isocalendar()[1]-semester.start.isocalendar()[1]
    
    for i in range(0, 40):
        instance, is_follow = TimeTable.objects.get_or_create(
            teacher = teacher, 
            semester = semester, 
            weekday = week[i%5],
            time = (i//5)%8+1
            )
        expand_inst_to_term(instance, week[i%5], weeks)