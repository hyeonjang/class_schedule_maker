'''
School informations - Semester, Hoilday, ...
'''
import time
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import update_classroom_timetable, add_user_to_hometeacher

# Create your models here.
class School(models.Model):
    '''
    School
    '''
    area = models.CharField(default="", max_length=64)
    name = models.CharField(default="", max_length=64)

    def __str__(self):
        return self.area + self.name + "초등학교"

    class Meta:
        unique_together = ('area', 'name')

class Holiday(models.Model):
    '''
    Hoilday Datatable
    '''
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    day = models.DateField()
    text = models.TextField(default="explanation")

    def __str__(self):
        return f"{self.day}"

class Term(models.Model):
    '''
    Semester Datatable
    '''
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
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

    @staticmethod
    def get_current():
        '''
        get current semester
        '''
        now = timezone.now()
        return Term.objects.filter(start__year=now.year).get()

    @staticmethod
    def get_current_week():
        today = timezone.datetime.today()
        year = today.year
        week = today.isocalendar()[1]
        str_time = time.strptime('{0} {1} 1'.format(year, week), '%Y %W %w')
        date = timezone.datetime(year=str_time.tm_year, month=str_time.tm_mon,
                                 day=str_time.tm_mday, tzinfo=timezone.utc).date()
        if timezone.datetime(year, 1, 4).isoweekday() > 4:
            # ISO 8601 where week 1 is the first week that has at least 4 days in
            # the current year
            date -= timezone.timedelta(days=7)
        return [date,
                date+timezone.timedelta(days=1),
                date+timezone.timedelta(days=2),
                date+timezone.timedelta(days=3),
                date+timezone.timedelta(days=4)]

    def get_start(self, start=None):
        '''
        return a starting day of this semester
        '''
        year = self.start.year
        week = self.start.isocalendar()[1]
        if start is not None:
            year = start.year
            week = start.isocalendar()[1]
        str_time = time.strptime('{0} {1} 1'.format(year, week), '%Y %W %w')
        date = timezone.datetime(year=str_time.tm_year, month=str_time.tm_mon, day=str_time.tm_mday, tzinfo=timezone.utc).date()
        if timezone.datetime(year, 1, 4).isoweekday() > 4:
            # ISO 8601 where week 1 is the first week that has at least 4 days in
            # the current year
            date -= timezone.timedelta(days=7)
        return date

    def get_week(self, start=None):
        '''
        return a starting week of this semester
        '''
        date = self.get_start(start)
        return [date, date+timezone.timedelta(days=1), date+timezone.timedelta(days=2), date+timezone.timedelta(days=3), date+timezone.timedelta(days=4)]

    def get_weeks_start_end(self):
        '''
        return only the monday and friday of whole semester
        '''
        starting_week = self.get_week()
        weeks = []
        duration = self.end - self.start
        for i in range(0, duration.days):
            if (i%7) == 0:
                week = (starting_week[0] + timezone.timedelta(days=i), starting_week[0] + timezone.timedelta(days=i+4))
                weeks.append(week)
        return weeks

    def get_count_of_weeks(self, start=None, end=None):
        '''
        return the count of weeks
        '''
        _start = self.start
        _end = self.end
        if start:
            _start = start
        if end:
            _end = end
        return (_end-_start).days//7

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

    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    grade = models.PositiveSmallIntegerField(default=1, choices=GRADE_RANGE)
    number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(20)])
    teacher = models.OneToOneField("accounts.User", on_delete=models.CASCADE, default=0, related_name="teacher_name")
    student_count = models.PositiveSmallIntegerField(default=1, null=True)

    class Meta:
        unique_together = ('grade', 'number')

    def __str__(self):
        return f'{self.grade}-{self.number}'

    def to_string(self):
        '''
        public string return function
        '''
        return f'{self.grade}-{self.number}'

    def save(self, *args, **kwargs):
        super(ClassRoom, self).save(*args, **kwargs)
        '''
        instantiate timetable
        '''
        update_classroom_timetable(Term.objects.all().get(), self.teacher, self)
        add_user_to_hometeacher(self.teacher, self)

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

    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=64)
    grade = models.PositiveSmallIntegerField(choices=GRADE_RANGE)
    count = models.IntegerField(default=272, validators=[MinValueValidator(64), MaxValueValidator(448)]) # 2018년도 교육과정 기준

    def __str__(self):
        return  self.name + f"({self.grade}G)"

    def to_string(self):
        '''
        public string return function
        '''
        return self.name

    class Meta:
        unique_together = ('name', 'grade')
