from django.contrib import admin

# Register your models here.
from student.models import Parent, Kids, Student


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'province', 'phone', 'email', 'debt', 'date_joined']


@admin.register(Kids)
class KidsAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'parent', 'grade', 'sick', 'birthday', 'is_active', 'transportation']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'province', 'phone', 'email', 'debt', 'date_joined', 'birthday',
                    'is_active', 'transportation']
