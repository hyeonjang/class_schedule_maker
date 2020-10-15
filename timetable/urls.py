'''
modul doc
'''
from django.urls import path, register_converter
from . import converters, views

register_converter(converters.DateConverter, 'date')

app_name = 'timetable'

urlpatterns = [
    path('<int:user_id>/<int:semester_id>/sub/create/', views.SubjectCreate.as_view(), name='sub_create'),
    path('<int:user_id>/<int:semester_id>/sub/reset/', views.SubjectReset.as_view(), name='sub_reset'),
    path('<int:user_id>/<int:semester_id>/<date:start>/<date:end>/sub/view/', views.SubjectView.as_view(), name='sub_view'),
    path('<int:user_id>/<int:semester_id>/<date:start>/<date:end>/sub/update/', views.SubjectUpdate.as_view(), name='sub_update'),

    path('<int:user_id>/<int:semester_id>/home/create/', views.HomeroomCreate.as_view(), name='home_create'),
    path('<int:user_id>/<int:semester_id>/home/reset/', views.HomeroomReset.as_view(), name='home_reset'),
    path('<int:user_id>/<int:semester_id>/<date:start>/<date:end>/home/view/', views.HomeroomView.as_view(), name='home_view'),
    path('<int:user_id>/<int:semester_id>/<date:start>/<date:end>/home/update/', views.HomeroomUpdate.as_view(), name='home_update'),

    path('<int:user_id>/<int:semester_id>/inv/create/', views.InvitedCreate.as_view(), name='inv_create'),
    path('<int:user_id>/<int:semester_id>/sub/reset/', views.InvitedReset.as_view(), name='inv_reset'),
    path('<int:user_id>/<int:semester_id>/<date:start>/<date:end>/inv/view/', views.InvitedView.as_view(), name='inv_view'),
    path('<int:user_id>/<int:semester_id>/<date:start>/<date:end>/inv/update/', views.InvitedUpdate.as_view(), name='inv_update'),

    path('semesters', views.TermListView.as_view(), name="term_view")
]
