from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import date, datetime
from datetime import timedelta
import calendar
from django.contrib import messages

# Create your views here.
from django.utils.safestring import mark_safe

from events.forms import EventFrom
from events.models import Event
from events.utils import EventCalendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
def events(request, slug=None):
    context = {}
    # Calendar
    calendar_date = get_date(request.GET.get('month', None))
    none_html_calendar = EventCalendar(calendar_date.year, calendar_date.month)
    html_calendar = none_html_calendar.formatmonth(withyear=True)
    context['calendar'] = mark_safe(html_calendar)
    context['prev_month'] = prev_month(calendar_date)
    context['next_month'] = next_month(calendar_date)
    # fetching data
    instance = Event()
    if slug:
        try:
            instance = Event.objects.get(slug=slug)
        except:
            messages.error(request, "Something went wrong ")
            return redirect("events:events")
    else:
        instance = Event()

    if request.method == 'GET':
        form = EventFrom(instance=instance)
        context['form'] = form
        return render(request, 'events/events.html', context)

    if request.method == 'POST':
        form = EventFrom(request.POST, instance=instance)

        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Operation Done!")
            return redirect("events:events")
        else:
            messages.error(request, "Error while saving")
            return redirect("events:events")

    return render(request, 'events/events.html', context)


@login_required
def event_details(request, slug):
    context = {}
    # fetch data
    try:
        event = Event.objects.get(slug=slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect("events:events")

    context['event'] = event

    if request.method == 'GET':
        form = EventFrom(instance=event)
        context['form'] = form
        return render(request, 'events/details.html', context)

    if request.method == 'POST':
        form = EventFrom(request.POST, instance=event)

        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'Event Updated')
            return redirect('events:events')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('events:events_details', event.slug)

    return render(request, 'events/details.html', context)


@login_required
def delete_event(request, slug):
    context = {}
    # fetch data
    try:
        Event.objects.get(slug=slug).delete()
        messages.success(request, "Event Deleted")
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect(request.META.get('HTTP_REFERER', 'events:events'))

    return redirect(request.META.get('HTTP_REFERER', 'events:events'))
