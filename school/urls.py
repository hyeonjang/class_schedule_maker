'''
School Information managemenet urls
'''
from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.admin, name='admin_view'),
    path('manage/term', views.TermManageListView.as_view(), name='manage_school'),
    path('manage/subject', views.SubjectManageListView.as_view(), name='manage_subject'),
    path('manage/classroom', views.ClassRoomManageListView.as_view(), name='manage_classroom'),
  
    path('filter_by_grade_cla/', views.ClassRoomGradeFilterView.as_view(), name='filter_classroom'),
    path('filter_by_grade_sub/', views.SubjectGradeFilterView.as_view(), name='filter_subject'),

    path('create_semester/', views.SemesterCreateView.as_view(), name='create_semester'),
    path('update_semester/<int:pk>', views.SemesterUpdateView.as_view(), name='update_semester'),
    path('delete_semester/<int:pk>', views.SemesterDeleteView.as_view(), name='delete_semester'),

    path('create_holiday/', views.HolidayCreateView.as_view(), name='create_holiday'),
    path('update_holiday/<int:pk>', views.HolidayUpdateView.as_view(), name='update_holiday'),
    path('delete_holiday/<int:pk>', views.HolidayDeleteView.as_view(), name='delete_holiday'),

    path('classrooms/', views.classrooms, name='classrooms'),
    path('create_classroom/', views.ClassRoomCreateView.as_view(), name='create_classroom'),
    path('update_classroom/<int:pk>', views.ClassRoomUpdateView.as_view(), name='update_classroom'),
    path('delete_classroom/<int:pk>', views.ClassRoomDeleteView.as_view(), name='delete_classroom'),

    path('create_subject/', views.SubjectCreateView.as_view(), name='create_subject'),
    path('update_subject/<int:pk>', views.SubjectUpdateView.as_view(), name='update_subject'),
    path('delete_subject/<int:pk>', views.SubjectDeleteView.as_view(), name='delete_subject'),
   
]

