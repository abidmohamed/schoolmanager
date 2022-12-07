from django.contrib import admin

# Register your models here.
from group.models import Group, GroupStudent, GroupTime


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'teacher', 'room', 'subject', 'name', 'group_type', 'date_created')
    search_fields = ['id', 'teacher', 'name', 'group_type']


@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'kid', 'student')


@admin.register(GroupTime)
class GroupTime(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'room', 'hallway', 'weekday', 'start_time', 'end_time')
