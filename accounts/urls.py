from django.urls import include, path
from .views import IndexView, HomeroomSignUpView, SubjectSignUpView, CustomLoginView, logout_view

urlpatterns = [
    path('accounts/', IndexView.as_view(), name='index'),
    path('accounts/signup/home/', HomeroomSignUpView.as_view(), name='homeroom_signup'),
    path('accounts/signup/sub/', SubjectSignUpView.as_view(), name='subject_signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
]