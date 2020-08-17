from django.urls import path
from . import views

urlpatterns = [
    path('classroom', views.classroom, name='classroom'),
    path('form', views.modify, name='form'),
    path('view', views.subject_view, name='view'),
]