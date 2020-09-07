'''
module doc
'''
from django.contrib import admin
from .models import SubjectTable, HomeTable
# Register your models here.
admin.site.register(SubjectTable)
admin.site.register(HomeTable)
