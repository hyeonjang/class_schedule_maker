from django.conf import settings
from django.db import models

# Create your models here.
class TimeTable(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classGrade = models.SmallIntegerField(default=0) #@@todo class room
    classNumber = models.SmallIntegerField(default=0)
    weekDay = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    semester = models.IntegerField(default=0)
    subject = models.CharField(max_length=50)

class sTerm(models.Model):
    code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

class sClass(models.Model):
    code = models.ForeignKey(TimeTable, on_delete=models.CASCADE) # actually class number

class sTeacher(models.Model):
    code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

class sSubject(models.Model):
    code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)