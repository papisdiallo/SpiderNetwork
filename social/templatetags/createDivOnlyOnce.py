from django import template
from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter(name="create_first_div_once")
def create_first_div_once(index):
    return True if index == 3 else False


@register.filter(name="create_second_div_once")
def create_second_div_once(index):
    return True if index == 1 else False


@register.filter(name="age")
def age(value):
    now = datetime.now()
    print(now)
    try:
        difference = now - value
        print("this is the difference", difference)
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}


@register.filter(name="two_last_comments")
def two_last_comments(queryset):
    return queryset.order_by("-id")[:2]
