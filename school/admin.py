from django.contrib import admin
from .models import Term, ClassRoom, Subject, Holiday, School

# Register your models here.
admin.site.register(School)

admin.site.register(Holiday)
admin.site.register(Term)
admin.site.register(ClassRoom)
admin.site.register(Subject)

