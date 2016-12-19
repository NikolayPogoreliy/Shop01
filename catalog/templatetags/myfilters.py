from django import template
register = template.Library()

@register.filter(name='get_value')
def get_value(value, arg):
    return value.get(arg)
