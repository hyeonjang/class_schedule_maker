'''
util functions
'''
from django.utils import timezone
import accounts
import school
import timetable

def add_user_to_hometeacher(user, classroom):
    accounts.models.HomeTeacher.objects.create(user=user, classroom=classroom) 

def create_homeroom_timetable(home):
    '''
    instantiating timetable when creating homeroom teacher
    '''
    semester = school.models.Term.get_current()
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

def create_subject_timetable(sub):
    '''
    instantiating timetable when create subject teacher
    '''
    semester = school.models.Term.get_current()
    mon_to_fri = semester.get_week()
    weeks = semester.get_count_of_weeks()

    bulk_tables = []
    for i in range(0, weeks):
        for j in range(0, 40):
            new_table = timetable.models.SubjectTable(
                teacher=accounts.models.User.get_from(teacher=sub),
                semester=semester,
                day=mon_to_fri[j%5] + timezone.timedelta(days=7*i),
                time=(j//5)%8+1,
            )
            bulk_tables.append(new_table)

    timetable.models.SubjectTable.objects.bulk_create(bulk_tables)

def create_invited_timetable(start, end, inv):
    '''
    instantiate timetable when create invited teacher
    '''
    semester = school.models.Term.get_current()
    mon_to_fri = semester.get_week(start)
    weeks = semester.get_count_of_weeks()

    bulk_tables = []
    for i in range(0, weeks+1):
        for j in range(0, 40):
            new_table = timetable.models.Invited(
                teacher=accounts.models.User.get_from(teacher=inv),
                semester=semester,
                day=mon_to_fri[j%5] + timezone.timedelta(days=7*i),
                time=(j//5)%8+1,
                )
            bulk_tables.append(new_table)

    timetable.models.Invited.objects.bulk_create(bulk_tables)
