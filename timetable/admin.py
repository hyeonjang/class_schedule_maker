'''
module doc
'''
from django.contrib import admin
from .models import SubjectTable, HomeTable

class SubjectInline(admin.TabularInline):
    '''
    '''
    model = SubjectTable
    fk_name = 'subject'

class HomeInline(admin.TabularInline):
    '''
    '''
    model = HomeTable
    fk_name = 'home'

class TableAdmin(admin.ModelAdmin):
    inlines = [
        SubjectInline,
        HomeInline,
    ]

# Register your models here.
admin.site.register(SubjectTable)
admin.site.register(HomeTable)
