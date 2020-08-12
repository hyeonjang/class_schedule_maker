from django.urls import path
from . import views

urlpatterns = [
    path('timetable', views.table_list, name='timetable'),
]