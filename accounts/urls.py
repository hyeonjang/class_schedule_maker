from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.login, name='logout'),
    path('password_change', views.login, name='password_change'),
    path('password_change', views.login, name='password_change'),
    path('password_change', views.login, name='password_change'),
    path('password_change', views.login, name='password_change'),
    path('password_change', views.login, name='password_change'),
]