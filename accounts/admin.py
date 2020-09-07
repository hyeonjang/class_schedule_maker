'''
custom user creation admin
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User

class UserAdmin(BaseUserAdmin):
    '''
    user admin management page
    '''
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Role', {'fields': ('is_homeroom',)}),
        ('Role', {'fields': ('is_subject',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'email', 'password1', 'password2',)}),
        ('Role', {'fields': ('is_homeroom',)}),
        ('Role', {'fields': ('is_subject',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
