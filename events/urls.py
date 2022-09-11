from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('events/', views.events, name='events'),
    path('events/details/<slug:slug>', views.event_details, name='events_details'),
    path('events/delete/<slug:slug>', views.delete_event, name='delete_event'),

]
