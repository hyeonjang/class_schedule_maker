'''
School informations - Semester, Hoilday, ...
'''
import time
from django.utils import timezone

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Holiday(models.Model):
    '''
    Hoilday Datatable
    '''
    day = models.DateField()

    def __str__(self):
        return f"{self.day}"

class Term(models.Model):
    '''
    Semester Datatable
    '''
    start = models.DateField()
    end = models.DateField()
    semester = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])

    def __str__(self):
        return f"{self.start.year}년도 {self.semester}학기"

    def save(self, *args, **kwargs):
        if self.start.month < 8:
            self.semester = 1
        else:
            self.semester = 2
        super(Term, self).save(*args, **kwargs)

    def get_starting_week(self):
        '''
        return a starting week of this semester
        '''
        year = self.start.year
        week = self.start.isocalendar()[1]
        str_time = time.strptime('{0} {1} 1'.format(year, week), '%Y %W %w')
        date = timezone.datetime(year=str_time.tm_year, month=str_time.tm_mon,
                                 day=str_time.tm_mday, tzinfo=timezone.utc)
        if timezone.datetime(year, 1, 4).isoweekday() > 4:
            # ISO 8601 where week 1 is the first week that has at least 4 days in
            # the current year
            date -= timezone.timedelta(days=7)
        return [date,
                date+timezone.timedelta(days=1),
                date+timezone.timedelta(days=2),
                date+timezone.timedelta(days=3),
                date+timezone.timedelta(days=4)]

    def get_weeks(self):
        '''
        return the count of weeks
        '''
        return self.end.isocalendar()[1]-self.start.isocalendar()[1]

class ClassRoom(models.Model):
    '''
    doct
    '''
    GRADE_RANGE = [
        (1, '1학년'),
        (2, '2학년'),
        (3, '3학년'),
        (4, '4학년'),
        (5, '5학년'),
        (6, '6학년'),
    ]

    grade = models.PositiveSmallIntegerField(default=1, choices=GRADE_RANGE)
    number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(20)])
    #teacher = models.OneToOneField("accounts.User", on_delete=models.CASCADE, default=1)
    #semester = models.ForeignKey(Term, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.grade}-{self.number}'

    def to_string(self):
        '''
        public string return function
        '''
        return f'{self.grade}-{self.number}'

    class Meta:
        unique_together = ('grade', 'number')

class Subject(models.Model):
    '''
    Subjects Model
    '''
    GRADE_RANGE = [
        (1, '1학년'),
        (2, '2학년'),
        (3, '3학년'),
        (4, '4학년'),
        (5, '5학년'),
        (6, '6학년'),
    ]

    name = models.CharField(max_length=64)
    grade = models.PositiveSmallIntegerField(choices=GRADE_RANGE)
    count = models.IntegerField(default=272, validators=[MinValueValidator(64), MaxValueValidator(448)]) # 2018년도 교육과정 기준

    def __str__(self):
        return  self.name + f'({self.grade}G)'

    def to_string(self):
        '''
        public string return function
        '''
        return self.name

    class Meta:
        unique_together = ('name', 'grade')
