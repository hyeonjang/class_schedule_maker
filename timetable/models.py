from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class day(models.Model):
    first = models.CharField(max_length=200)
    second = models.CharField(max_length=200)
    third = models.CharField(max_length=200)
    fourth = models.CharField(max_length=200)
    fifth = models.CharField(max_length=200)
    sixth = models.CharField(max_length=200)

class Timetable(models.Model):
    classNum = models.CharField(max_length=200)
    Mon = day()
    Tues = day()
    Wed = day()
    Thurs = day()
    Fri = day()
    Sat = day()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.classNum