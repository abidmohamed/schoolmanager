from django import template

register = template.Library()


@register.filter
def remove_leading_zeros(value):
    try:
        return int(value)
    except ValueError:
        return value
