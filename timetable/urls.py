from django.urls import path
from . import views

#url(r'^user/(?P<user_id>\d+)/profile/$', 'yourapp.views.view', name='user_url')

urlpatterns = [
    path('<int:user_id>/create', views.SubjectCreate.as_view(), name='create'),
    path(r'(?P<username>\d+)/view/$', views.SubjectView.as_view(), name='view'),
    #path(r'(?P<username>\d+)/update/$(?P<pk>\d+)/$', views.SubjectUpdate.as_view(), name='update'),
    path('update', views.SubjectUpdate.as_view(), name='update'),
    
    # path('<int:year>/view/<int:week>/',   views.SubjectView.as_view(), name='view'),
]