'''
modul doc
'''
from django.urls import path
from . import views

#url(r'^user/(?P<user_id>\d+)/profile/$', 'yourapp.views.view', name='user_url')

app_name = 'timetable'

urlpatterns = [
    path('<int:user_id>/sub/view/', views.SubjectView.as_view(), name='sub_view'),
    path('<int:user_id>/sub/create/', views.SubjectCreate.as_view(), name='sub_create'),
    path('<int:user_id>/sub/update/', views.SubjectUpdate.as_view(), name='sub_update'),
    path('<int:user_id>/home/view/', views.HomeRoomView.as_view(), name='home_view'),
    path('<int:user_id>/home/create/', views.HomeRoomCreate.as_view(), name='home_create'),
    path('<int:user_id>/home/update/', views.HomeRoomUpdate.as_view(), name='home_update'),
]
