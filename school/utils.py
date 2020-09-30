'''
util functions
'''
import accounts
import timetable

def update_classroom_timetable(semester, home, classroom):
    '''
    instantiating timetable when creating classroom
    '''
    tables = timetable.models.HomeTable.objects.filter(semester=semester, teacher=home)
    tables.update(classroom=classroom)

def add_user_to_hometeacher(user, classroom):
    accounts.models.HomeTeacher.objects.create(user=user, classroom=classroom) 
