from django import template
from django.template import Template

register = template.Library()


@register.filter(name='gender')
def decode_gender(code):
    if code == 'M':
        return 'Male'
    elif code == 'F':
        return 'Female'
    elif code == 'O':
        return 'Other'
    else:
        return 'Not to say'
