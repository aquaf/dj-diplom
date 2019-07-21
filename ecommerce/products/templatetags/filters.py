
from django import template

register = template.Library()

@register.filter
def convert_stars(stars):
    return '★'*stars