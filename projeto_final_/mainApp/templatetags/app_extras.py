import calendar
from django import template
from django.utils.html import format_html
from django.template import Variable, VariableDoesNotExist
from django.utils.translation import gettext as _
from datetime import datetime, timedelta

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
                            <div class="col-sm-3 p-0 pl-3">\
                                <p class="font-weight-bold text-{}">{}</p>\
                            </div>\
                            <div class="col-sm-9 p-0"> <p>{}</p> \
                            </div>\
                        </div>\
                    </div>', color, feature, feature_name)

@register.simple_tag
def add_one_day(dateIn):
    date = datetime.strptime(dateIn, "%Y-%m-%d")
    modified_date = date + timedelta(days=1)
    return datetime.strftime(modified_date, "%Y-%m-%d")
    

def check(feature_name):
    return format_html('<div class="col-sm-3 room-detail-item">\
            <i class="fa fa-check text-green" aria-hidden="yes"></i> {}\
            </div>', feature_name)

def cross(feature_name):
     return format_html('<div class="col-sm-3 room-detail-item">\
            <i class="fa fa-times text-primary" aria-hidden="no"></i> {}\
            </div>', feature_name)   

@register.filter
def month_name(month_number):
    return _(calendar.month_name[month_number])

@register.filter
def get_item(dictionaty, key):
    return dictionaty.get(key)

# @register.simple_tag
# def get_type_notification(notification):
#     if notification[len(notification)-1] == "agreement_request":
#         return True
#     elif notification[len(notification)-1] == "invoice":
#         return False
#     elif notification[len(notification)-1] == "warning":
#         return None