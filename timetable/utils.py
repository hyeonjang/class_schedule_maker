'''
util functions
'''
from django.utils import timezone
from .models import HomeTable

def expand_to_term(instance, day, weeks):
    """
    copy to term
    """
    for i in range(1, weeks):
        copy = HomeTable.objects.get(time=instance.time, weekday=day+timezone.timedelta(days=7*i))
        copy.semester = instance.semester
        copy.subject = instance.subject
        copy.save()
