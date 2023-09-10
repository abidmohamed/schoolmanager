from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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

    # API end points
    path('token/', TokenObtainPairView.as_view(), name='login_token'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

]
