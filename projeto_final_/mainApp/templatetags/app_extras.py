from django import template
from django.utils.html import format_html
register = template.Library()

@register.simple_tag
def get_checkmark(feature, feature_name):
    #takes a given object boolean property and returns the apropriate checkmark icon and text
    #based on it's value
    if type(feature) == int or type(feature) == float:
        print(feature)
        if feature > 0:
            return numberIten('green', feature, feature_name)
        else:
            return numberIten('primary', feature, feature_name)
    else:
        if feature:
            return check(feature_name)
        else:
            return cross(feature_name)  

def numberIten(color, feature, feature_name):
    return format_html('<div class="col-sm-3 room-detail-item">\
                        <div class="row">\
                            <div class="col-sm-1">\
                                <p class="font-weight-bold text-{}">{}</p>\
                            </div>\
                            <div class="col-sm-8 pl-1"> <p>{}</p> \
                            </div>\
                        </div>\
                    </div>', color, feature, feature_name)
def check(feature_name):
    return format_html('<div class="col-sm-3 room-detail-item">\
            <i class="fa fa-check text-green" aria-hidden="yes"></i> {}\
            </div>', feature_name)

def cross(feature_name):
     return format_html('<div class="col-sm-3 room-detail-item">\
            <i class="fa fa-times text-primary" aria-hidden="no"></i> {}\
            </div>', feature_name)   


