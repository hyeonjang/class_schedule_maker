'''
Abstract TimeTable model
'''
from django.db import models
from django.utils import timezone

from accounts.models import User
from school.models import Term, ClassRoom, Subject

# Create your models here.
class TimeTable(models.Model):
    '''
    Abstract TimeTable model
    '''
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True) # works in view.py
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True) #user choice
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True) #user choice
    weekday = models.DateField(default=timezone.now, null=True, blank=True) # works in view.py
    time = models.SmallIntegerField(default=0, blank=True) # works in view.py

    class Meta:
        unique_together = ['weekday', 'time', 'classRoom']
        abstract = True

    def __str__(self):
        if self.classRoom:
            result = self.classRoom.c_str()+'반 '+f'{self.time}교시 '
        else:
            result = f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        result += f', {self.weekday}'
        return result

class SubjectTable(TimeTable):
    """
    for Subject Teacher
    """
    def __str__(self):
        result = super().teacher
        if self.classRoom:
            result += self.classRoom.c_str()+'반 '+f'{self.time}교시 '
        else:
            result = f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        result += f', {self.weekday}'
        return result

class HomeTable(TimeTable):
    """
    for Homeroom Teacher
    """
    # sub_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subject')
      