from django.contrib import admin

# Register your models here.
from teacher.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ['user', 'profile', 'subject'
        , 'name', 'address', 'phone', 'email'
        , 'major', 'certificate', 'salary'
        , 'birthday', 'is_active', 'date_joined'
              ]
