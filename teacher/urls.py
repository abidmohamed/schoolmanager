from . import views
from django.urls import path

app_name = 'teachers'

urlpatterns = [
    # subjects
    path('subjects', views.subjects, name='subjects'),
    path('subjects/details/<str:pk>', views.subject_details, name='subject_details'),
    # teachers
    path('teachers', views.teachers, name='teachers'),
    path('teachers/update/<slug:slug>', views.update_teacher, name='update_teacher'),
    path('teachers/details/<slug:slug>', views.teacher_details, name='teacher_details'),
    path('teachers/details/group-pdf/<slug:slug>', views.teacher_groups_pdf, name='teacher_groups_pdf'),
    # Teacher account
    path('attendances/', views.teacher_attendances, name='teacher_attendances'),

]
