"""scheduling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from accounts.models import User, InvitedTeacher
from school.models import Term

def home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        current_week = Term.get_current_week()
        if request.user.user_type is User.SUPERVISOR:
            return reverse_lazy('school:manage_school', kwargs={'user_id':request.user.id})
        elif request.user.user_type is User.HOMEROOM:
            return redirect(reverse_lazy('timetable:home_view', kwargs={'user_id':request.user.id, 'start':current_week[0], 'end':current_week[4]}))
        elif request.user.user_type is User.SUBJECT:
            return redirect(reverse_lazy('timetable:sub_view', kwargs={'user_id':request.user.id, 'start':current_week[0], 'end':current_week[4]}))
        elif request.user.user_type is User.INVITED:
            semester = Term.get_current()
            week = semester.get_week(InvitedTeacher.get_from(request.user).start)
            return redirect(reverse_lazy('timetable:inv_view', kwargs={'user_id':request.user.id, 'start':week[0], 'end':week[4]}))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('accounts.urls')),
    path('school/', include('school.urls')),
    path('timetable/', include('timetable.urls')),
]
