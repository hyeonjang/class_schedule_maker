'''
doc
'''
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/home/', views.HomeroomSignUpView.as_view(), name='homeroom_signup'),
    path('signup/sub/', views.SubjectSignUpView.as_view(), name='subject_signup'),
    path('signup/inv/', views.InvitedSignUpView.as_view(), name='invited_signup'),
]