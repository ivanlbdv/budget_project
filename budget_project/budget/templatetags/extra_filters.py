from django import template

register = template.Library()


@register.filter
def subtract(inc, exp):
    try:
        return float(inc) - float(exp)
    except (ValueError, TypeError):
        return 0
