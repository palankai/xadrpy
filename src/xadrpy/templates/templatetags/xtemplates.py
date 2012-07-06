from django import template
from xadrpy.utils.jsonlib import JSONEncoder
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def JSON(value):
    return mark_safe(JSONEncoder().encode(value))