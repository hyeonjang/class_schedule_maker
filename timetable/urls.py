from django.urls import path
from . import views

urlpatterns = [
    path('classroom', views.classroom, name='classroom'),
    path('subject', views.subject, name='subject')
]