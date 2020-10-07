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