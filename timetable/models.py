from django.conf import settings
from django.db import models

# Create your models here.
class TimeTable(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classGrade = models.SmallIntegerField(default=0)
    classNumber = models.SmallIntegerField(default=0)
    classRoom = models.SmallIntegerField(default=0)
    subject = models.CharField(max_length=50)
    time = models.SmallIntegerField(default=0)
    weekday = models.CharField(max_length=50)

# class Term(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class ClassRoom(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class Teacher(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class Subject(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)