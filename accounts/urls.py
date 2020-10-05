'''
doc
'''
from django.urls import path
from .views import (
    CustomLoginView,
    logout_view,
    HomeroomSignUpView,
    SubjectSignUpView,
    InvitedSignUpView,
)

urlpatterns = [
    path('accounts/login', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/signup/home/', HomeroomSignUpView.as_view(), name='homeroom_signup'),
    path('accounts/signup/sub/', SubjectSignUpView.as_view(), name='subject_signup'),
    path('accounts/signup/inv/', InvitedSignUpView.as_view(), name='invited_signup'),
]