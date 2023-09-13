from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Subject(models.Model):
    # Basic Fields
    name = models.CharField(null=True, blank=True, max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)
    n_sessions = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    CERTIFICATION = [
        ('License', 'License'),
        ('Master', 'Master'),
        ('Doctor', 'Doctor'),
    ]
    # Related Fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="teachers", null=True)
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub_teachers", null=True)
    # Basic Fields
    name = models.CharField(_("Name"), null=True, blank=True, max_length=200)
    address = models.CharField(_("Address"), null=True, blank=True, max_length=200)
    phone = models.CharField(_("Phone"), null=True, blank=True, max_length=100)
    email = models.CharField(_("Email"), null=True, blank=True, max_length=100)
    major = models.CharField(_("Major"), null=True, blank=True, max_length=100)
    certificate = models.CharField(_("Certificate"), choices=CERTIFICATION, blank=True, max_length=100)
    salary = models.DecimalField(_("Salary"), max_digits=10, decimal_places=2, null=True, blank=True)
    birthday = models.DateField(_("BirthDay"), null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    date_joined = models.DateField(_("Date Joined"), null=True)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.major,)

    def get_absolute_url(self):
        return reverse('parent-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.major, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.name, self.major, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Teacher, self).save(*args, **kwargs)




