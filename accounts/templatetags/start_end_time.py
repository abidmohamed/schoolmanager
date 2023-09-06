# Create a custom filter in one of your Django app's templatetags files
from django import template

register = template.Library()


@register.filter
def get_start_time(time_slot):
    return time_slot.split(' - ')[0]


@register.filter
def get_end_time(time_slot):
    return time_slot.split(' - ')[1]
