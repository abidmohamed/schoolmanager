from datetime import datetime, timedelta
from calendar import HTMLCalendar

from django.shortcuts import redirect

from events.models import Event


class EventCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(EventCalendar, self).__init__()

    def formatday(self, day, events):
        """
        Return a day as a table cell.
        """
        events_per_day = events.filter(day__day=day, )
        d = '<ul class="list-group text-center">'
        for event in events_per_day:
            url = event.get_absolute_url()
            delete_url = event.delete_url()
            if event.event_type == "TEACHERS":
                d += f'<li class="list-group-item list-group-item-primary"><a href="{url}" >{event}</a>'
                d += f'<br>'
                d += f'<a class="btn btn-danger" href="{delete_url}" onclick="return confirm("Are you sure?")">'
                d += f'<i class="fa-solid fa-trash-can"></i></a>'
                d += f'</li>'
            if event.event_type == "MANAGEMENT":
                d += f'<li class="list-group-item list-group-item-success"><a href="{url}" >{event}</a>'
                d += f'<br>'
                d += f'<a class="btn btn-danger" href="{delete_url}" onclick="return confirm("Are you sure?")">'
                d += f'<i class="fa-solid fa-trash-can"></i></a>'
                d += f'</li>'
            if event.event_type == "MEDIA":
                d += f'<li class="list-group-item list-group-item-info"><a href="{url}" >{event}</a>'
                d += f'<br>'
                d += f'<a class="btn btn-danger" href="{delete_url}" onclick="return confirm("Are you sure?")">'
                d += f'<i class="fa-solid fa-trash-can"></i></a>'
                d += f'</li>'
            if event.event_type == "TRANSPORT":
                d += f'<li class="list-group-item list-group-item-warning"><a href="{url}" >{event}</a>'
                d += f'<br>'
                d += f'<a class="btn btn-danger" href="{delete_url}" onclick="return confirm("Are you sure?")">'
                d += f'<i class="fa-solid fa-trash-can"></i></a>'
                d += f'</li>'
            if event.event_type == "PAYMENT":
                d += f'<li class="list-group-item list-group-item-danger"><a href="{url}" >{event}</a>'
                d += f'<br>'
                d += f'<a class="btn btn-danger" href="{delete_url}" onclick="return confirm("Are you sure?")">'
                d += f'<i class="fa-solid fa-trash-can"></i></a>'
                d += f'</li>'
        d += '</ul>'
        if day != 0:
            return f"<td class=''><span class='date'>{day}</span><ul class='list-group'> {d} </ul></td>"
        return '<td class="text-dark"></td>'

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr class="text-dark"> {week} </tr>'

    def formatmonth(self, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(day__month=self.month, day__year=self.year)

        cal = f'<br><table border="0" cellpadding="0" cellspacing="0" class="calendar text-dark">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'</table>\n'
        return cal
