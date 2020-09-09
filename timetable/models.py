'''
Abstract TimeTable model
'''
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from accounts.models import User
from school.models import Term, ClassRoom, Subject

# Create your models here.
class TimeTable(models.Model):
    '''
    Abstract TimeTable model
    '''
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True) # works in view.py
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True) #user choice
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True) #user choice
    weekday = models.DateField(default=timezone.now, null=True, blank=True) # works in view.py
    time = models.SmallIntegerField(default=0, blank=True) # works in view.py

    class Meta:
        unique_together = (('weekday', 'time', 'teacher'),)
        abstract = True

    def __str__(self):
        if self.classroom:
            result = self.classroom.c_str()+'반 '+f'{self.time}교시 '
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
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='main_sub_teacher')

    def __str__(self):
        result = super().teacher.to_string() + ', '
        if self.classroom:
            result += self.classroom.c_str()+'반, '+f'{self.time}교시 '
        else:
            result += f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        result += f', {self.weekday}'
        return result

    def copy_to_hometable(self):
        queryset = HomeTable.objects.filter(
            classroom=self.classroom,
            weekday=self.weekday,
            time=self.time,
            )
        # print(instance)
        # if queryset.exists():
        #     if (queryset.get().sub_teacher is not self.teacher):
        #         raise ValidationError(f"already {queryset.get().sub_teacher}")
        queryset.update(sub_teacher=self.teacher, subject=self.subject)

    def save(self, *args, **kwargs):
        '''
        save with copy to Hometable
        '''
        self.copy_to_hometable()
        super(SubjectTable, self).save(*args, **kwargs)

class Invited(TimeTable):
    """
    for Invited Teacher
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='invited_teacher')
    available = models.BooleanField()

class HomeTable(TimeTable):
    """
    for Homeroom Teacher
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='main_home_teacher')
    sub_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subject_teacher')
    inv_teacher = models.OneToOneField(Invited, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        result = super().teacher.to_string() + ', '
        if self.classroom:
            result += self.classroom.c_str()+'반, '+f'{self.time}교시, '
        else:
            result += f'{self.time}교시, '
        if self.subject:
            result += self.subject.name + ', '
        if self.sub_teacher:
            result += self.sub_teacher.to_string() + ', '
        result += f'{self.weekday}'
        return result

