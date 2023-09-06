from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth paths
    path('', views.login, name='login'),
    path('check-group', views.group_check, name='group_check'),
    path('logout', views.logout, name='logout'),

    # User
    path('users/', views.users, name='users'),

    # Dashboards
    path('dashboard', views.dashboard, name='dashboard'),
    path('teacher-dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent-dashboard', views.parent_dashboard, name='parent_dashboard'),
    path('student-dashboard', views.student_dashboard, name='student_dashboard'),

]
