# arbitration/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Получает значение из словаря по ключу."""
    return d.get(key)
