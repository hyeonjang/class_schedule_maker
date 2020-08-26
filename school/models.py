from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Term(models.Model):
    start    = models.DateField()
    end      = models.DateField()
    semester = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])

    def __str__(self):
        return f"{self.start.year}년도 {self.semester}학기"       

    def save(self, *args, **kwargs):
        if self.start.month<9:
            self.semester = 1
        else:
            self.semester = 2
        super(Term, self).save(*args, **kwargs)

class ClassRoom(models.Model):
    classGrade  = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(6)])
    classNumber = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])

    def __str__(self):
        return f'{self.classGrade}-{self.classNumber}'

class Subject(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name    