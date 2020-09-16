'''
util functions
'''
from django.utils import timezone
from accounts.models import User
from timetable.models import HomeTable

def create_classroom_timetable(semester, classroom):
    '''
    instantiating timetable when creating classroom
    '''
    mon_to_fri = semester.get_starting_week()
    weeks = semester.get_count_of_weeks()

    for i in range(0, weeks):
        for j in range(0, 40):
            HomeTable.objects.create(
                classroom=classroom,
                teacher=User.objects.get(pk=classroom.teacher.pk),
                semester=semester,
                weekday=mon_to_fri[j%5] + timezone.timedelta(days=7*i),
                time=(j//5)%8+1,
                )
