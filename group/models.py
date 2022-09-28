from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
# Create your models here.
from student.models import Kids, Student
from teacher.models import Subject, Teacher


class Room(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="rooms", null=True)
    # basic
    name = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name


class Group(models.Model):
    GROUP_TYPES = [
        ('KIDS', 'KIDS'),
        ('ADULTS', 'ADULTS'),
    ]
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="created_groups", null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, related_name="teacher_groups", null=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, related_name="group_rooms", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="group_subjects", null=True)
    # basic
    name = models.CharField(null=True, blank=True, max_length=200)
    group_type = models.CharField(choices=GROUP_TYPES, blank=True, max_length=100)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.room, self.uniqueId)

    def get_absolute_url(self):
        return reverse('parent-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.room, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.name, self.room, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Group, self).save(*args, **kwargs)


class GroupStudent(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="group_students", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="items", null=True)
    # One of them will be occupied
    kid = models.ForeignKey(Kids, on_delete=models.DO_NOTHING, related_name="kid_group", null=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name="student_group", null=True)


class GroupTime(models.Model):
    WEEKDAYS = [
        ('SATURDAY', 'SATURDAY'),
        ('SUNDAY', 'SUNDAY'),
        ('MONDAY', 'MONDAY'),
        ('TUESDAY', 'TUESDAY'),
        ('WEDNESDAY', 'WEDNESDAY'),
        ('THURSDAY', 'THURSDAY'),
        ('FRIDAY', 'FRIDAY'),
    ]
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="group_times", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="times", null=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, related_name="times_rooms", null=True)
    # basic
    hallway = models.CharField(null=True, blank=True, max_length=200)
    weekday = models.CharField(choices=WEEKDAYS, blank=True, max_length=100)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

