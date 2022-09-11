from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4


# Create your models here.
class Event(models.Model):
    EVENT_TYPES = [
        ("TEACHERS", "TEACHERS"),  # PRIMARY
        ("MANAGEMENT", "MANAGEMENT"),  # SUCCESS
        ("MEDIA", "MEDIA"),  # INFO
        ("TRANSPORT", "TRANSPORT"),  # WARNING
        ("PAYMENT", "PAYMENT"),  # DANGER
    ]
    # related
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="events", null=True)
    # basic
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    event_type = models.CharField(choices=EVENT_TYPES, max_length=200)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.day, self.event_type, self.uniqueId)

    def get_absolute_url(self):
        return reverse('events:events_details', kwargs={'slug': self.slug})

    def delete_url(self):
        return reverse('events:delete_event', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.day, self.event_type, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.day, self.event_type, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Event, self).save(*args, **kwargs)
