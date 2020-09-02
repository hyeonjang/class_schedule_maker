from django.db import models
from django.conf import settings
from django.utils import timezone

from accounts.models import User
from school.models import Term, ClassRoom, Subject

# Create your models here.
class TimeTable(models.Model):
    teacher   = models.ForeignKey(User, on_delete=models.CASCADE)
    semester  = models.ForeignKey(Term,      on_delete=models.CASCADE, blank=True) # works in view.py
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True) #user choice
    subject   = models.ForeignKey(Subject,   on_delete=models.CASCADE, null=True, blank=True) #user choice
    weekday   = models.DateField(default=timezone.now, null=True, blank=True) # works in view.py
    time      = models.SmallIntegerField(default=0, blank=True) # works in view.py
    created_time = models.DateTimeField(default=timezone.now, null=True, blank=True) # works in view.py

    class Meta:
        unique_together = ['weekday', 'time']

    def __str__(self):
        if self.classRoom:
            result = self.classRoom.c_str()+'반 '+f'{self.time}교시 '
        else: 
            result = f'{self.time}교시 '
        if self.subject:
            result += self.subject.name
        result += f', {self.weekday}'
        return result

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('view', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.created_time = timezone.now()
        super(TimeTable, self).save(*args, **kwargs)