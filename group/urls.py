from . import views
from django.urls import path

app_name = 'groups'

urlpatterns = [
    # rooms
    path('rooms', views.rooms, name='rooms'),
    # groups
    path('groups', views.groups, name='groups'),
    path('groups/select-kids/<slug:slug>', views.select_kids, name='select_kids'),
    path('groups/select-students/<slug:slug>', views.select_students, name='select_students'),
    path('groups/details/<slug:slug>', views.group_details, name='group_details'),
    path('groups/delete/<str:id>', views.delete_group_item, name='delete_group_item'),
    # times
    path('groups-times', views.groups_times, name='groups_times'),
    path('groups-times/update/<str:pk>', views.update_groups_times, name='update_groups_times'),
    path('groups-times/delete/<str:pk>', views.delete_groups_times, name='delete_groups_times'),
    path('groups-times/pdf', views.times_pdf, name='times_pdf'),

]