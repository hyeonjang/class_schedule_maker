from django.urls import path
from .views import signup, logout, UserLogin

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/' , UserLogin.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    # path('password_change', views.login, name='password_change'),
    # path('password_change', views.login, name='password_change'),
    # path('password_change', views.login, name='password_change'),
    # path('password_change', views.login, name='password_change'),
    # path('password_change', views.login, name='password_change'),
]