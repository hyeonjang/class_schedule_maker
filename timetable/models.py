from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class TimeTable(models.Model):
    studentID = models.CharField(max_length=200)
    studentName = models.CharField(max_length=200)
    courses = models.CharField(max_length=200)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.studentID

