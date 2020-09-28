'''
util functions
'''
from django.utils import timezone
import school
import accounts
from .models import HomeTable

def expand_to_term(instance, teacher, day, weeks):
    """
    copy to term
    """
    for i in range(1, weeks):
        copy = HomeTable.objects.get(teacher=teacher, time=instance.time, weekday=day+timezone.timedelta(days=7*i))
        copy.semester = instance.semester
        copy.subject = instance.subject
        copy.save()

def create_information(user):
    '''
    Return TimeTable information to Templates
    '''
    information = dict()

    teacher = accounts.models.HomeTeacher.objects.get(user=user)
    semester = school.models.Term.get_current()
    subjects = school.models.Subject.objects.filter(grade=teacher.get_grade())

    for subject in subjects:
        weeks = semester.get_weeks_start_end()
        count_per_week = []

        for week in weeks:
            start = week[0].strftime("%Y-%m-%d")
            end = week[1].strftime("%Y-%m-%d")
            count_per_week.append(
                HomeTable.objects.filter(teacher=user, subject=subject, weekday__range=(start, end)).count()
                )
        dic = {subject:[
            subject.grade,
            count_per_week,
            HomeTable.objects.filter(teacher=user, subject=subject).count(),
            subject.count
            ]}

        information.update(dic)
    return information

def create_list_for_weeks():
    semester = school.models.Term.get_current()
    weeks = semester.get_weeks_start_end()
    week_list = []
    for days in weeks:
        week_list.append((days[0].strftime("%Y-%m-%d"), days[1].strftime("%Y-%m-%d")))
    return week_list