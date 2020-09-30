'''
modul doc
'''
from django.urls import path, register_converter
from . import converters, views

#url(r'^user/(?P<user_id>\d+)/profile/$', 'yourapp.views.view', name='user_url')

register_converter(converters.DateConverter, 'date')

app_name = 'timetable'

urlpatterns = [
    path('<int:user_id>/sub/create/', views.SubjectCreate.as_view(), name='sub_create'),
    path('<int:user_id>/<date:start>/<date:end>/sub/view/', views.SubjectView.as_view(), name='sub_view'),
    path('<int:user_id>/<date:start>/<date:end>/sub/update/', views.SubjectUpdate.as_view(), name='sub_update'),
    path('<int:user_id>/home/create/', views.HomeRoomCreate.as_view(), name='home_create'),
    path('<int:user_id>/<date:start>/<date:end>/home/view/', views.HomeRoomView.as_view(), name='home_view'),
    path('<int:user_id>/<date:start>/<date:end>/home/update/', views.HomeRoomUpdate.as_view(), name='home_update'),
    path('<int:user_id>/inv/create/', views.InvitedCreate.as_view(), name='inv_create'),
    path('<int:user_id>/<date:start>/<date:end>/inv/view/', views.InvitedView.as_view(), name='inv_view'),
    path('<int:user_id>/<date:start>/<date:end>/inv/update/', views.InvitedUpdate.as_view(), name='inv_update'),


]
