from django.urls import path
from . import views

urlpatterns = [
    path('classroom', views.classroom, name='classroom'),
    path('subject_form', views.subject_form, name='subject_form'),
    path('subject_view', views.subject_view, name='subject_view'),
]