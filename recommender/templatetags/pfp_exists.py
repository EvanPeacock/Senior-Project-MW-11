from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.filter(name='pfp_exists')
def pfp_exists(filename):
    if default_storage.exists(filename + '.jpg'):
        return filename
    else:
        return 'defaultPFP'