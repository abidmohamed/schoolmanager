from django.contrib import admin

# Register your models here.
from attendance.models import StudentAttendance, StudentAttendanceItem, EmployeeAttendance, EmployeeAttendanceItem, \
    EmployeeLeaveItem, TeacherAttendanceItem, TeacherLeaveItem, SessionCounter, TeacherSessionCounter


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'attendance_date', 'attendance_time', 'status']


@admin.register(StudentAttendanceItem)
class StudentAttendanceItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance', 'kid', 'student', 'status']


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance_date', 'status']


@admin.register(EmployeeAttendanceItem)
class EmployeeAttendanceItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance', 'employee', 'attendance_time', 'status']


@admin.register(EmployeeLeaveItem)
class EmployeeLeaveItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance', 'employee', 'leave_time', 'status']


@admin.register(TeacherAttendanceItem)
class TeacherAttendanceItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance', 'teacher', 'attendance_time', 'status']


@admin.register(TeacherLeaveItem)
class TeacherLeaveItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'attendance', 'teacher', 'leave_time', 'status']


@admin.register(SessionCounter)
class SessionCounterAdmin(admin.ModelAdmin):
    list_display = ['user', 'kid', 'student', 'group', 'subject', 'start_date', 'end_date', 'n_sessions']


@admin.register(TeacherSessionCounter)
class TeacherSessionCounterAdmin(admin.ModelAdmin):
    list_display = ['user', 'teacher', 'group', 'subject', 'start_date', 'end_date', 'n_sessions']
