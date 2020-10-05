'''
util functions
'''
from django.utils import timezone
import accounts
import school
import timetable

def create_list_for_weeks():
    semester = school.models.Term.get_current()
    weeks = semester.get_weeks_start_end()
    week_list = []
    for days in weeks:
        week_list.append((days[0], days[1]))
    return week_list

def create_homeroom_timetable(home, semester):
    '''
    instantiating timetable when creating homeroom teacher
    '''
    mon_to_fri = semester.get_week()
    weeks = semester.get_count_of_weeks()

    bulk_tables = []
    for i in range(0, weeks):
        for j in range(0, 40):
            new_table = timetable.models.HomeTable(
                teacher=accounts.models.User.get_from(teacher=home),
                semester=semester,
                day=mon_to_fri[j%5] + timezone.timedelta(days=7*i),
                time=(j//5)%8+1,
                )
            bulk_tables.append(new_table)

    timetable.models.HomeTable.objects.bulk_create(bulk_tables)