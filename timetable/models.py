from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class TimeTable(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classGrade = models.SmallIntegerField(default=0)
    classNumber = models.SmallIntegerField(default=0)
    classRoom = models.SmallIntegerField(default=0)
    subject = models.CharField(max_length=50)
    time = models.SmallIntegerField(default=0)
    weekday = models.CharField(max_length=50)
    created_time = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('view', args=[str(self.id)])
    
    def mod(self, subject):
        self.subject = subject

    def save(self, *args, **kwargs):
        self.created_time = timezone.now()
        super(TimeTable, self).save(*args, **kwargs)
        print("new saved at {}", self.created_time)

# class Term(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class ClassRoom(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class Teacher(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class Subject(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)