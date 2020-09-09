from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from school.models import ClassRoom, Subject

class User(AbstractUser):
    '''
    todo doc
    '''
    HOMEROOM = 1
    SUBJECT = 2
    INVITED = 3
    SUPERVISOR = 4
    ADMIN = 5

    USER_TYPE_CHOICES = [
        (HOMEROOM, 'homeroom'),
        (SUBJECT, 'subject'),
        (INVITED, 'invited'),
        (SUPERVISOR, 'supervisor'),
        (ADMIN, 'admin'),
    ]
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)

    def to_string(self):
        '''
        return name
        '''
        return self.username

class HomeTeacher(models.Model):
    '''
    homeroom
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    classroom = models.OneToOneField(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class SubjectTeacher(models.Model):
    '''
    homeroom
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subject = models.ManyToManyField(Subject, related_name='teaching_subject')
    
    def __str__(self):
        return self.user.username

class InvitedTeacher(models.Model):
    '''
    Invited
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    start = models.DateField()
    end = models.DateField()
