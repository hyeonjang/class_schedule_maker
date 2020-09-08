from django.contrib import admin
from .models import User, HomeTeacher, SubjectTeacher

# Register your models here.
admin.site.register(User)
admin.site.register(HomeTeacher)
admin.site.register(SubjectTeacher)
