from django.urls import path
from . import views

#url(r'^user/(?P<user_id>\d+)/profile/$', 'yourapp.views.view', name='user_url')

urlpatterns = [
    path(r'(?P<userid>\d+)/sub/create/$', views.SubjectCreate.as_view(), name='sub_create'),
    path(r'(?P<userid>\d+)/sub/view/$', views.SubjectView.as_view(), name='sub_view'),
    path(r'(?P<userid>\d+)/sub/update/$', views.SubjectUpdate.as_view(), name='sub_update'),
    
    path(r'(?P<userid>\d+)/home/create/$', views.HomeRoomCreate.as_view(), name='home_create'),
    path(r'(?P<userid>\d+)/home/view/$', views.HomeRoomView.as_view(), name='home_view'),
    path(r'(?P<userid>\d+)/home/update/$', views.SubjectUpdate.as_view(), name='home_update'),
]