'''
util functions
'''
import school
import accounts
from .models import HomeTable



def create_list_for_weeks():
    semester = school.models.Term.get_current()
    weeks = semester.get_weeks_start_end()
    week_list = []
    for days in weeks:
        week_list.append((days[0].strftime("%Y-%m-%d"), days[1].strftime("%Y-%m-%d")))
    return week_list