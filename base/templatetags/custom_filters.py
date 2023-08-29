from django import template
from ..utils.utils import get_domain_from_url
register = template.Library()

@register.filter(name='extract_path')
def extract_path(value):
    if get_domain_from_url(value):
        return value.split(get_domain_from_url(value))[-1]
    return ''

@register.filter(name="extract_domain")
def extract_domain(value):
    return get_domain_from_url(value)

@register.filter(name="page_availability_from_bool")
def page_availability_from_bool(value):
    bool_to_text = {
        True: "Działa",
        False: "Nie działa",
        None: "Brak danych"
    }
    return bool_to_text[value]

@register.filter(name="color_class_from_bool")
def color_class_from_bool(value):
    bool_to_text = {
        True: "green-text",
        False: "red-text",
        None: "black-text"
    }
    return bool_to_text[value]

@register.filter(name="color_class_from_rel_attribute")
def color_class_from_rel_attribute(value):
    rel_to_text = {
        'dofollow': "purple-text",
        'nofollow': "black-text",
    }
    return rel_to_text[value]