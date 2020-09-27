'''
util functions
'''
from django.utils import timezone
import accounts
import timetable

def create_homeroom_timetable(semester, classroom):
    '''
    instantiating timetable when creating classroom
    '''
    mon_to_fri = semester.get_starting_week()
    weeks = semester.get_count_of_weeks()

    bulk_tables = []
    for i in range(0, weeks):
        for j in range(0, 40):
            new_table = timetable.models.HomeTable(
                classroom=classroom,
                teacher=accounts.models.User.objects.get(pk=classroom.teacher.pk),
                semester=semester,
                weekday=mon_to_fri[j%5] + timezone.timedelta(days=7*i),
                time=(j//5)%8+1,
                )
            bulk_tables.append(new_table)

    timetable.models.HomeTable.objects.bulk_create(bulk_tables)

def add_user_to_hometeacher(user, classroom):
    accounts.models.HomeTeacher.objects.create(user=user, classroom=classroom) 
