from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ( None, {'fields': ('name', 'email', 'password')}),
        ('Role', {'fields': ('is_homeroom', 'classRoom', ) }),
        ('Role', {'fields': ('is_subject', 'assigned_subjects_number', 'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6') }),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        ( None,  {'fields': ('name', 'email', 'password1', 'password2',)}),
        ('Role', {'fields': ('is_homeroom', 'classRoom', ) }),
        ('Role', {'fields': ('is_subject', 'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6') }),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)