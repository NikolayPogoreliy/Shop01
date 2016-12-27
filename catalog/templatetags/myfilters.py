from django import template
register = template.Library()

@register.filter(name='get_value')
def get_value(value, arg):
    return value.get(arg)


@register.filter
def any_value(value):
    if value:
        return any(value)
