from timetable.utils import expand_inst_to_term, mon_to_fri
from timetable.models import TimeTable
from .models import Term

def instantiate_term_timetable(semester, classRoom):
        week = mon_to_fri(semester.start.year, semester.start.isocalendar()[1])
        weeks = semester.end.isocalendar()[1]-semester.start.isocalendar()[1]
        
        for i, in range(0, 39):
            instance = TimeTable.objects.create(classRoom=classRoom)
            instance.semester = semester
            instance.time = (i//5)%8+1 # row major table input
            instance.weekday = week[i%5]
            instance.save()
            expand_inst_to_term(instance, week[i%5], weeks)