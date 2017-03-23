from django import template
from django.template.defaulttags import register


register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key).date.strftime("%m-%d")
    
@register.filter
def get_month(dictionary, key):
    return str(dictionary.get(key))
    
@register.filter
def get_sum(dictionary, key):
    return dictionary.get(key)
    
