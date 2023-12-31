from django import template
from ..api.utils import get_domain_from_url
register = template.Library()


@register.filter(name='extract_path')
def extract_path(value):
    if get_domain_from_url(value):
        return value.split(get_domain_from_url(value))[-1]
    return ''


@register.filter(name="extract_domain")
def extract_domain(value):
    return get_domain_from_url(value)


@register.filter(name="availability_from_bool")
def availability_from_bool(value):
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
        None: "black-text",
    }
    return rel_to_text[value]


@register.filter(name="none_to_default")
def none_to_default(value):
    if value == None:
        return 'Brak danych'
    return value


@register.filter(name="background_color_class_from_change_attribute")
def background_color_class_from_change_attribute(value):
    bool_to_text = {
        True: "purple-background",
        False: "pass",
    }
    return bool_to_text[value]


@register.filter(name="is_invoice_paid_info_from_bool")
def is_invoice_paid_info_from_bool(value):
    bool_to_text = {
        True: "Opłacona",
        False: "Nieopłacona",
    }
    return bool_to_text[value]


@register.filter(name='invert_boolean')
def invert_boolean(value):
    return not value


@register.filter(name='text_color_from_position_change')
def text_color_from_position_change(value):
    if value < 0:
        return 'red-text'
    elif value == 0:
        return 'pass'
    else:
        return 'green-text'

@register.filter(name='format_poisition_change')
def format_poisition_change(value):
    if value > 0:
        return f'+{value}'
    elif value == 0:
        return '-'
    return value