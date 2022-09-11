from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth paths
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # User
    path('users/', views.users, name='users'),

    # Dashboard
    path('dashboard', views.dashboard, name='dashboard'),

]
