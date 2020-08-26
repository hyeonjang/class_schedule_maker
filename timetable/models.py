from django.db import models
from django.conf import settings
from django.utils import timezone

from school.models import Term, ClassRoom, Subject

# Create your models here.
class TimeTable(models.Model):
    teacher   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    semester  = models.ForeignKey(Term,      on_delete=models.CASCADE, default=1)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    subject   = models.ForeignKey(Subject,   on_delete=models.CASCADE, null=True, blank=True)
    weekday   = models.DateField()
    time      = models.SmallIntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['weekday', 'time']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('view', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        self.created_time = timezone.now()
        super(TimeTable, self).save(*args, **kwargs)
        print("new saved at {}", self.created_time)

