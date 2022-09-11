from . import views
from django.urls import path

app_name = 'employees'

urlpatterns = [
    path('employees', views.employees, name='employees'),
    path('employees/details/<slug:slug>', views.employee_details, name='employee_details'),
    # Role
    path('roles', views.roles, name='roles'),
    path('roles/details/<str:pk>', views.role_details, name='role_details'),

]
