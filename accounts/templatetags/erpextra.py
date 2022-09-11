from django import template
from django.contrib.auth.models import Group

register = template.Library()


# filter for groups
@register.filter(name='has_group')
def has_group(user, group_name):
    is_allowed = False
    # print(group_name)
    # print(group_name.split(','))
    # Creating a list of strings
    group_name = group_name.split(',')
    for name in group_name:
        # print(name)
        # print(''.join(name.split()))
        # removing white spaces
        name = ''.join(name.split())
        group = Group.objects.get(name=name)
        if group in user.groups.all():
            is_allowed = True
    return is_allowed
