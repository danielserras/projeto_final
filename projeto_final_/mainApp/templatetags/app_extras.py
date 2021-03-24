from django import template
from django.utils.html import format_html
from django.template import Variable, VariableDoesNotExist
from django.utils.translation import gettext as _

register = template.Library()

@register.simple_tag
def get_checkmark(feature, feature_name):
    #takes a given object boolean property and returns the apropriate checkmark icon and text
    #based on it's value
    if feature:
        return check(_(feature_name))
    else:
        return cross(_(feature_name))  

@register.simple_tag
def get_number_beds(feature, feature_name):
    if feature > 0:
        return numberIten('green', feature, _(feature_name))
    else:
        return numberIten('primary', feature, _(feature_name))

@register.simple_tag
def resolve(lookup, target):
    try:
        print('hello')
        return Variable(lookup).resolve(target)
    except VariableDoesNotExist:
        return None

def numberIten(color, feature, feature_name):
    return format_html('<div class="col-sm-3 room-detail-item">\
                        <div class="row">\
                            <div class="col-sm-2 p-0 pl-3">\
                                <p class="font-weight-bold text-{}">{}</p>\
                            </div>\
                            <div class="col-sm-10 p-0"> <p>{}</p> \
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


