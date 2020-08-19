from django.urls import path
from . import views

urlpatterns = [
    path('classroom', views.classroom, name='classroom'),
    path('create', views.create, name='create'),
    path('modify', views.modify, name='modify'),
    path('view', views.subject_view, name='view'),
]