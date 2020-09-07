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
from django.urls import path, include
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.is_admin:
            return render(request, 'index.html')
            #return redirect('school:admin_view')
        elif request.user.is_homeroom:
            return render(request, 'timetable/sub_create')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='index'),

    path('', include('accounts.urls')),
    path('school/', include('school.urls')),
    path('timetable/', include('timetable.urls')),

]
