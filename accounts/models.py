from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         (1, 'homeroom'),
#         (2, 'subject'),
#         (3, 'instructor'),
#         (4, 'head'),
#     )

#     user_type  = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

def is_member(user, group_name, role_name):
    return user.groups.filter(name__in=[group_name, role_name]).exists()

def group_exist(group_name, role_name):
    return Group.objects.filter(name__in=[group_name, role_name]).exists()