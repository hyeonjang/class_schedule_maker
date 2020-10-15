'''
util functions
'''
import school

def create_list_for_weeks(semester):
    if semester is None:
        print("no semester")
        return
    weeks = semester.get_weeks_start_end()
    week_list = []
    for days in weeks:
      week_list.append((days[0], days[1]))
    return week_list
