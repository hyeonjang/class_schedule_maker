'''
Abstract TimeTable model
'''
from django.db import models
from django.utils import timezone

from accounts.models import User
from school.models import Term, Holiday, ClassRoom, Subject

# Create your models here.
class TimeTable(models.Model):
    '''
    Abstract TimeTable model
    '''
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True) # works in view.py
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True) #user choice
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True) #user choice
    day = models.DateField(default=timezone.now, null=True, blank=True) # works in view.py
    time = models.SmallIntegerField(default=0, blank=True) # works in view.py
    is_event_or_holi = models.BooleanField(default=False)

    class Meta:
        unique_together = (('day', 'time', 'teacher'),)
        abstract = True

    def __str__(self):
        if self.classroom:
            result = self.classroom.to_string()+'반 '+f'{self.time}교시 '
        else:
            result = f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        result += f', {self.day}'
        return result

    def save(self, *args, **kwargs):
        if Holiday.objects.filter(day=self.day):
            self.is_event_or_holi = True
        return super(TimeTable, self).save(*args, **kwargs)

    def get_count_of_subject(self, sub):
        self.objects.filter(subject=sub).count()

class SubjectTable(TimeTable):
    """
    for Subject Teacher
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='main_sub_teacher')

    def __str__(self):
        result = super().teacher.to_string() + ', '
        if self.classroom:
            result += self.classroom.to_string()+'반, '+f'{self.time}교시 '
        else:
            result += f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        return result

    def copy_to_hometable(self):
        '''
        copy to HomeTable
        '''
        # 1. reset reference tables
        HomeTable.objects.filter(sub_teacher=self, day=self.day, time=self.time).update(sub_teacher=None, subject=None)
        # 2. find and update
        qs = HomeTable.objects.filter(classroom=self.classroom, day=self.day, time=self.time)
        qs.update(sub_teacher=self, subject=self.subject)

    def save(self, *args, **kwargs):
        self.copy_to_hometable()
        super(SubjectTable, self).save(*args, **kwargs)

class Invited(TimeTable):
    """
    for Invited Teacher
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='invited_teacher')

    def __str__(self):
        result = super().teacher.to_string() + ', '
        if self.classroom:
            result += self.classroom.to_string()+'반, '+f'{self.time}교시 '
        else:
            result += f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        return result

    def copy_to_hometable(self):
        '''
        copy to HomeTable
        '''
        # 1. reset reference tables
        HomeTable.objects.filter(inv_teacher=self, day=self.day, time=self.time).update(inv_teacher=None, subject=None)
        # 2. find and update
        qs = HomeTable.objects.filter(classroom=self.classroom, day=self.day, time=self.time)
        qs.update(inv_teacher=self, subject=self.subject)

    def save(self, *args, **kwargs):
        self.copy_to_hometable()
        super(Invited, self).save(*args, **kwargs)

class HomeTable(TimeTable):
    """
    for Homeroom Teacher
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='main_home_teacher')
    sub_teacher = models.OneToOneField(SubjectTable, on_delete=models.SET_NULL, null=True, blank=True)
    inv_teacher = models.OneToOneField(Invited, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        result = super().teacher.to_string() + ', '
        if self.classroom:
            result += self.classroom.to_string()+'반, '+f'{self.time}교시, '
        else:
            result += f'{self.time}교시, '
        if self.subject:
            result += self.subject.name + ', '
        result += f'{self.day}'
        return result

    def save(self, *args, **kwargs):
        if (self.sub_teacher or self.inv_teacher) is not None:
            return
        return super(HomeTable, self).save(*args, **kwargs)
