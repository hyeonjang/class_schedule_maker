'''
util functions
'''
from django.core.exceptions import ValidationError
import accounts
import timetable

def update_classroom_timetable(semester, home, classroom):
    '''
    instantiating timetable when creating classroom
    '''
    tables = timetable.models.HomeTable.objects.filter(semester=semester, teacher=home)
    tables.update(classroom=classroom)

def add_user_to_hometeacher(user, classroom):
    if user.user_type != accounts.models.User.HOMEROOM:
        raise ValidationError("User Type is Not homeroomteacher")

    accounts.models.HomeTeacher.objects.filter(classroom=classroom).update(classroom=None)
    instance = accounts.models.HomeTeacher.objects.get(user=user)
    instance.classroom = classroom
    instance.save()
