from django import template
from schedule_app.models import Schedule

register = template.Library()

@register.filter
def get_day_name(day_code):
    for day in Schedule.DAYS_OF_WEEK:
        if day[0] == day_code:
            return day[1]
    return day_code

@register.filter
def get_timeslot_display(timeslot):
    for slot in Schedule.TIMESLOTS:
        if slot[0] == timeslot:
            return slot[1]
    return timeslot

@register.filter
def split(value, arg):
    return value.split(arg) 