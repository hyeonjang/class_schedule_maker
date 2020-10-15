from django.contrib import admin
from .models import School, Term, ClassRoom, Subject, Holiday

# Register your models here.
admin.site.register(School)
admin.site.register(Term)
admin.site.register(Holiday)
admin.site.register(ClassRoom)
admin.site.register(Subject)
