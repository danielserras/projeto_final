from django import template
from django.utils.html import format_html
register = template.Library()

@register.simple_tag
def get_checkmark(feature, feature_name):
    #takes a given object boolean property and returns the apropriate checkmark icon and text
    #based on it's value
    if feature:
        return format_html('<div class="col-sm-3 room-detail-item">\
        <i class="fa fa-check text-green" aria-hidden="yes"></i> {}\
        </div>', feature_name)
    else:
        return format_html('<div class="col-sm-3 room-detail-item">\
        <i class="fa fa-times text-primary" aria-hidden="no"></i> {}\
        </div>', feature_name)   


