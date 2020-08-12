from django.conf import settings
from django.db import models

from django.contrib.postgres.fields import ArrayField


# Create your models here.
class TimeTable(models.Model):
    Teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classGrade = models.SmallIntegerField(default=0)
    classNumber = models.SmallIntegerField(default=0)
    Table = ArrayField(
                ArrayField(
                    ArrayField(models.CharField(max_length=50 ,default=''))
                )
            )

