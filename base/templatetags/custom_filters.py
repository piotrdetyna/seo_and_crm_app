from django import template
from ..utils.utils import get_domain_from_url
register = template.Library()

@register.filter(name='extract_path')
def extract_path(value):
    if get_domain_from_url(value):
        return value.split(get_domain_from_url(value))[-1]
    return ''