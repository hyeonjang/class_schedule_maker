'''
Abstract TimeTable model
'''
from django.db import models
from django.utils import timezone
from django.core.validators import ValidationError
from accounts.models import User
from school.models import Term, Holiday, ClassRoom, Subject

# Create your models here.
class TimeTable(models.Model):
    '''
    Abstract TimeTable model
    '''
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True) # works in view.py
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True) #user choice
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True) #user choice
    day = models.DateField(default=timezone.now, null=True, blank=True) # works in view.py
    time = models.SmallIntegerField(default=0, blank=True) # works in view.py
    is_event_or_holi = models.BooleanField(default=False)

    class Meta:
        unique_together = (('day', 'time', 'teacher'),)
        abstract = True

    def __reset__(self):
        self.subject = None

    def __str__(self):
        if self.classroom:
            result = self.classroom.to_string()+'반 '+f'{self.time}교시 '
        else:
            result = f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        result += f', {self.day}'
        return result

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

    def __copy_to_hometable__(self):
        '''
        copy to HomeTable
        '''
        # 1. reset reference tables
        HomeTable.objects.filter(sub_teacher=self, day=self.day, time=self.time).update(sub_teacher=None, subject=None)
        # 2. find and update
        if self.classroom:
            qs = HomeTable.objects.filter(classroom=self.classroom.pk, day=self.day, time=self.time)
            if qs.get().inv_teacher:
                raise ValidationError(f"{qs} {self.day} {self.time}교시에 {qs.get().inv_teacher}가 존재합니다")
            if qs.get().sub_teacher:
                raise ValidationError(f"{qs} {self.day} {self.time}교시에 {qs.get().inv_teacher}가 존재합니다")
            qs.update(sub_teacher=self, subject=self.subject)

    def __reset__(self):
        super(SubjectTable, self).__reset__()
        self.classroom = None

    def save(self, *args, **kwargs):
        # 1. holiday
        if Holiday.objects.filter(day=self.day):
            self.is_event_or_holi = True
        else:
            self.is_event_or_holi = False
        if self.is_event_or_holi is True:
            self.__reset__()

        # 2. copy
        super(SubjectTable, self).save(*args, **kwargs)
        self.__copy_to_hometable__()

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

    def __copy_to_hometable__(self):
        '''
        copy to HomeTable
        '''
        # 1. reset reference tables
        HomeTable.objects.filter(inv_teacher=self, day=self.day, time=self.time).update(inv_teacher=None, subject=None)
        # 2. find and update
        if self.classroom:
            qs = HomeTable.objects.filter(classroom=self.classroom.pk, day=self.day, time=self.time)
            if qs.get().inv_teacher:
                raise ValidationError(f"{qs} {self.day} {self.time}교시에 {qs.get().inv_teacher}가 존재합니다")
            if qs.get().sub_teacher:
                raise ValidationError(f"{qs} {self.day} {self.time}교시에 {qs.get().inv_teacher}가 존재합니다")
            qs.update(inv_teacher=self, subject=self.subject)

    def __reset__(self):
        super(Invited, self).__reset__()
        self.classroom = None

    def save(self, *args, **kwargs):

        if Holiday.objects.filter(day=self.day):
            self.is_event_or_holi = True
        else:
            self.is_event_or_holi = False

        if self.is_event_or_holi is True:
            self.__reset__()

        self.__copy_to_hometable__()
        return super(Invited, self).save(*args, **kwargs)

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

    def __reset__(self):
        super(HomeTable, self).__reset__()
        if self.sub_teacher:
            print("home", self.classroom)
            self.sub_teacher.__reset__()
            print("sub", self.classroom)
        if self.inv_teacher:
            self.inv_teacher.__reset__()

    def save(self, *args, **kwargs):
        # 1. for holiday
        self.is_event_or_holi = False
        if Holiday.objects.filter(day=self.day):
            self.is_event_or_holi = True

        if self.is_event_or_holi is True:
            self.__reset__()

        if self.sub_teacher is not None or self.inv_teacher is not None:
            return

        # 2. validation checking
        # if self.classroom is None:
            # raise ValidationError(f"{self.day} {self.time}교시 학급정보가 입력되지 않았습니다.")
        return super(HomeTable, self).save(*args, **kwargs)
