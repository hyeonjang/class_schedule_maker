from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

from school.models import ClassRoom, Subject

#https://dev-yakuza.github.io/ko/django/custom-user-model/
class UserManager(BaseUserManager):
    def create_user(self, email, name, classRoom, subject, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), 
            name=name, 
            classRoom=classRoom, 
            subject=subject,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, classRoom, subject, password):
        user = self.create_user(
            email,
            name=name,
            password=password,
            classRoom=classRoom, 
            subject=subject,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    name = models.CharField(default='', max_length=53)

    is_active = models.BooleanField(default=True)
    
    # permssion and role
    is_admin = models.BooleanField(default=False)
    is_subject = models.BooleanField(default=True)
    is_homeroom = models.BooleanField(default=True)

    classRoom = models.OneToOneField(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    ### permission properties
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    ### get properties
    def get_classRoom(self):
        return self.classRoom.pk