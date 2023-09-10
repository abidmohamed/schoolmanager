from . import views
from django.urls import path

app_name = 'students'

urlpatterns = [
    # parents
    path('parents', views.parents, name='parents'),
    path('parents/update/<slug:slug>', views.update_parent, name='update_parent'),
    path('parents/details/<slug:slug>', views.parent_details, name='parent_details'),
    path('My-kids', views.parent_kids, name='parent_kids'),
    path('My-kids/details/<slug:slug>', views.parent_kid_details, name='parent_kid_details'),

    # Kids
    path('kids', views.kids, name='kids'),
    path('kids/details/<slug:slug>', views.kid_details, name='kid_details'),
    path('kids/details/group-pdf/<slug:slug>', views.kid_groups_pdf, name='kid_groups_pdf'),
    path('kids/update/<slug:slug>', views.kid_update, name='kid_update'),
    # Students
    path('students', views.students, name='students'),
    path('students/update/<slug:slug>', views.update_student, name='update_student'),
    path('students/details/<slug:slug>', views.student_details, name='student_details'),
    path('students/details/group-pdf/<slug:slug>', views.groups_pdf, name='groups_pdf'),
    # Transportation
    path('transportation', views.transportation_list, name='transportation'),
    path('transportation/print', views.transportation_pdf, name='transportation_pdf'),

    # API URLS
    path('api/My-kids/', views.ParentKidsAPIView.as_view(), name='api_parent_kids'),
    path('api/My-kids/details/<slug:slug>', views.ParentKidDetailsView.as_view(), name='api_parent_kid_details'),

]
