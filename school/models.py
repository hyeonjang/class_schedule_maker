from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Holiday(models.Model):
    day = models.DateField()

    def __str__(self):
        return f"{self.day}"

class Term(models.Model):
    start    = models.DateField()
    end      = models.DateField()
    semester = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])

    def __str__(self):
        return f"{self.start.year}년도 {self.semester}학기"       

    def save(self, *args, **kwargs):
        if self.start.month<8:
            self.semester = 1
        else:
            self.semester = 2
        super(Term, self).save(*args, **kwargs)

class ClassRoom(models.Model):
    GRADE_RANGE = {
        (1, '1학년'),
        (2, '2학년'),
        (3, '3학년'),
        (4, '4학년'),
        (5, '5학년'),
        (6, '6학년'),
   }
    
    grade  = models.PositiveSmallIntegerField(default=1, choices=GRADE_RANGE)
    number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(20)])
    teacher = models.OneToOneField("accounts.User", on_delete=models.CASCADE, default=1)
    semester = models.ForeignKey(Term, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.grade}-{self.number}'
    
    def c_str(self):
        return f'{self.grade}-{self.number}'

    class Meta:
        unique_together = ('grade', 'number')

class Subject(models.Model):
    GRADE_RANGE = {
        (1, '1학년'),
        (2, '2학년'),
        (3, '3학년'),
        (4, '4학년'),
        (5, '5학년'),
        (6, '6학년'),
   }

    name = models.CharField(max_length=64)
    grade = models.PositiveSmallIntegerField(choices=GRADE_RANGE)
    count = models.IntegerField(default=272, validators=[MinValueValidator(128), MaxValueValidator(448)]) # 2018년도 교육과정 기준
    
    teacher1 = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='one')
    teacher2 = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='two')
    teacher3 = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='three')
    teacher4 = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='four')
   
    semester = models.ForeignKey(Term, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return  self.name + f'({self.grade}G)'

    def to_string(self):
        return self.name

    class Meta:
        unique_together = ('name', 'grade')
