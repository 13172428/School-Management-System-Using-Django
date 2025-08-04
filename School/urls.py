# School/urls.py
from django.urls import path
from . import views
from .views import StudentDashboard, TeacherDashboard, ParentDashboard



urlpatterns = [
    path('', views.home, name='home'),  # Fix: pass the view reference, not call it
    path('login/', views.unified_login_view, name='login'),  # Add slash and remove parentheses

    path('dashboard/student/', StudentDashboard.as_view(), name='student_dashboard'),
    path('dashboard/teacher/', TeacherDashboard.as_view(), name='teacher_dashboard'),
    path('dashboard/parent/',  ParentDashboard.as_view(),  name='parent_dashboard'),

    path('logout/', views.logout_view, name='logout'),
]
