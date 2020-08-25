from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class TimeTable(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classRoom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=50, blank=True)
    time = models.SmallIntegerField(default=0)
    weekday = models.CharField(max_length=50)
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['weekday', 'time']

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

class ClassRoom(models.Model):
    classGrade  = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(6)])
    classNumber = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])

    def __str__(self):
        return f'{self.classGrade}-{self.classNumber}'

class RoomNumber(models.Model):
    
# class Teacher(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

# class Subject(models.Model):
#     code = models.ForeignKey(TimeTable, on_delete=models.CASCADE)