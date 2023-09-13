from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4

# Create your models here.
from employee.models import Employee
from student.models import Student, Parent
from teacher.models import Teacher


class StudentPayment(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="student_payments", null=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name="payments", null=True)
    # basic
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()
    note = models.TextField(blank=True, null=True)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.student)

    def get_absolute_url(self):
        return reverse('pay-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.student, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.student, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(StudentPayment, self).save(*args, **kwargs)


class ParentPayment(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="parent_payments", null=True)
    parent = models.ForeignKey(Parent, on_delete=models.DO_NOTHING, related_name="payments", null=True)
    # basic
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()
    note = models.TextField(blank=True, null=True)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.parent)

    def get_absolute_url(self):
        return reverse('pay-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.parent, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.parent, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(ParentPayment, self).save(*args, **kwargs)


class Payroll(models.Model):
    PAYROLL_TYPE = [
        ('EMPLOYEE', 'EMPLOYEE'),
        ('TEACHER', 'TEACHER')
    ]
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="payrolls", null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='employee_payroll', null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, related_name='teacher_payroll', null=True)
    # basic fields
    pay_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_type = models.CharField(choices=PAYROLL_TYPE, blank=True, max_length=100)
    paid = models.BooleanField(default=False)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.uniqueId)

    def get_absolute_url(self):
        return reverse('pay-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{}'.format(self.uniqueId))

        self.slug = slugify('{}'.format(self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Payroll, self).save(*args, **kwargs)
