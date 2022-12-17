from . import views
from django.urls import path

app_name = 'attendances'

urlpatterns = [
    path('attendances/attendances-details/<slug:slug>/<str:item>', views.attendances_details, name='attendances_details'),
    # attendances students & teachers
    path('attendances', views.attendances, name='attendances'),
    path('stats', views.attendance_stats, name='attendance_stats'),
    path('attendances/group-attendances/<slug:slug>', views.group_attendances, name='group_attendances'),
    path('attendances/group-attendances/students-attendances/<slug:slug>', views.students_attendances, name='students_attendances'),
    path('attendances/group-attendances/students-confirm-attendance/<slug:slug>', views.students_confirm_attendance, name='students_confirm_attendance'),
    path('attendances/group-attendances/students-attendances-details/<slug:slug>', views.students_attendances_details,
         name='students_attendances_details'),
    # # Leaving
    path('attendances/teacher-leave/<slug:slug>', views.teacher_leave,
         name='teacher_leave'),

    path('attendances/teacher-leave/teacher-confirm-leave/<slug:slug>', views.teacher_confirm_leave,
         name='teacher_confirm_leave'),



    # Employee Attendances
    path('employee-attendances', views.employee_attendances, name='employee_attendances'),
    path('employee-attendances/employee-list-attendance/<slug:slug>', views.employee_list_attendance, name='employee_list_attendance'),
    path('employee-attendances/employee-list-leave/<slug:slug>', views.employee_list_leave, name='employee_list_leave'),
    path('employee-attendances/employee-list-attendance/employees-confirm-attendance/<slug:slug>', views.employees_confirm_attendance,
         name='employees_confirm_attendance'),
    path('employee-attendances/employee-list-leave/employees-confirm-leave/<slug:slug>', views.employees_confirm_leave,
         name='employees_confirm_leave'),
    path('employee-attendances/employee-list/employees-attendances-details/<slug:slug>', views.employees_attendance_details,
         name='employees_attendance_details'),
]