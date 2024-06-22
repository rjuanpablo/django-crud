from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),

    #path('profile/', views.profile, name='profile'),
    #path('settings/', views.settings, name='settings'),
    #path('password_change/', views.password_change, name='password_change'),
]
