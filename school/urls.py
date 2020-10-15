'''
School Information managemenet urls
'''
from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('school/', views.SchoolSignUp.as_view(), name='school_signup'),
    path('<int:school_id>/manage/term', views.TermManageListView.as_view(), name='manage_semester'),
    path('<int:school_id>/manage/subject', views.SubjectManageListView.as_view(), name='manage_subject'),
    path('<int:school_id>/manage/classroom', views.ClassRoomManageListView.as_view(), name='manage_classroom'),

    path('<int:school_id>/filter_by_grade_cla/', views.ClassRoomGradeFilterView.as_view(), name='filter_classroom'),
    path('<int:school_id>/filter_by_grade_sub/', views.SubjectGradeFilterView.as_view(), name='filter_subject'),

    path('semesters/', views.semesters, name='semesters'),
    path('<int:school_id>/create_semester/', views.SemesterCreateView.as_view(), name='create_semester'),
    path('<int:school_id>/update_semester/<int:pk>', views.SemesterUpdateView.as_view(), name='update_semester'),
    path('<int:school_id>/delete_semester/<int:pk>', views.SemesterDeleteView.as_view(), name='delete_semester'),

    path('holidays/', views.holidays, name='holidays'),
    path('<int:school_id>/create_holiday/', views.HolidayCreateView.as_view(), name='create_holiday'),
    path('<int:school_id>/update_holiday/<int:pk>', views.HolidayUpdateView.as_view(), name='update_holiday'),
    path('<int:school_id>/delete_holiday/<int:pk>', views.HolidayDeleteView.as_view(), name='delete_holiday'),

    path('classrooms/', views.classrooms, name='classrooms'),
    path('<int:school_id>/create_classroom/', views.ClassRoomCreateView.as_view(), name='create_classroom'),
    path('<int:school_id>/update_classroom/<int:pk>', views.ClassRoomUpdateView.as_view(), name='update_classroom'),
    path('<int:school_id>/delete_classroom/<int:pk>', views.ClassRoomDeleteView.as_view(), name='delete_classroom'),

    path('subjects/', views.subjects, name='subjects'),
    path('<int:semester_id>/create_subject/', views.SubjectCreateView.as_view(), name='create_subject'),
    path('<int:semester_id>/update_subject/<int:pk>', views.SubjectUpdateView.as_view(), name='update_subject'),
    path('<int:semester_id>/delete_subject/<int:pk>', views.SubjectDeleteView.as_view(), name='delete_subject'),
]
