from django import template

register = template.Library()


@register.filter(name="create_first_div_once")
def create_first_div_once(index):
    return True if index == 3 else False


@register.filter(name="create_second_div_once")
def create_second_div_once(index):
    return True if index == 1 else False
