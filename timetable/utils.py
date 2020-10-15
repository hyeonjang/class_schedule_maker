'''
util functions
'''
import school

def create_list_for_weeks(semester):
    if semester is None:
        print("no semester") #@@todo delete
        return
    weeks = semester.get_weeks_start_end()
    list_weeks = []
    dict_week = dict()
    for days in weeks:
        dict_week = {"pk":semester.pk, "days":(days[0], days[1])}
        list_weeks.append(dict_week)
    return list_weeks
