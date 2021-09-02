from django import template

register = template.Library()

@register.filter
def key_to_value(value, key):
    return value.get(key, '')