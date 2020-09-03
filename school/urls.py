from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path(r'(?P<userid>\d+)/manage/$', views.ManageView.as_view(), name='manage_view'),
]
