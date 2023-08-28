from django import template

register = template.Library()

from .custom_filters import extract_path

register.filter('extract_path', extract_path)   