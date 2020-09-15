'''
util functions
'''
from django.utils import timezone
from timetable.models import TimeTable

def create_classroom_timetable(semester, classroom):
    '''
    instantiating timetable when creating classroom
    '''
    mon_to_fri = semester.return_starting_week()
    weeks = semester.end.isocalendar()[1]-semester.start.isocalendar()[1]

    for i in range(0, weeks):
        for j in range(0, 40):
            TimeTable.objects.create(
                classRoom=classroom,
                semester=semester,
                weekday=mon_to_fri[j%5] + timezone.timedelta(days=7*i),
                time=(j//5)%8+1,
                )
