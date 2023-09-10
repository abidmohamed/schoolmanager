from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
# Create your models here.
from employee.models import Employee
from group.models import Group
from student.models import Kids, Student


# # Student
from teacher.models import Teacher, Subject


class StudentAttendance(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="attendance_user", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="attendance", null=True)
    # basic fields
    attendance_date = models.DateField()
    attendance_time = models.TimeField(null=True)
    status = models.BooleanField(default=False)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.group, self.attendance_date, self.uniqueId)

    def get_absolute_url(self):
        return reverse('parent-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.group, self.attendance_date, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.group, self.attendance_date, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(StudentAttendance, self).save(*args, **kwargs)


class StudentAttendanceItem(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="student_attendance_user", null=True)
    attendance = models.ForeignKey(StudentAttendance, on_delete=models.CASCADE, related_name="attendance_students",
                                   null=True)
    # # One of them will be occupied
    kid = models.ForeignKey(Kids, on_delete=models.DO_NOTHING, related_name="kid_attendance", null=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name="student_attendance", null=True)
    status = models.BooleanField(default=False)


# # Employee
class EmployeeAttendance(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="attendance_employee_user", null=True)
    # basic fields
    attendance_date = models.DateField()
    status = models.BooleanField(default=False)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.attendance_date, self.uniqueId)

    def get_absolute_url(self):
        return reverse('attendance-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.attendance_date, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.attendance_date, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(EmployeeAttendance, self).save(*args, **kwargs)


class EmployeeAttendanceItem(models.Model):
    STATUS = (('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT'), ('UNAPPROVED ABSENT', 'UNAPPROVED ABSENT'), ('MISSION', 'MISSION'))
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="attendance_employee_item", null=True)
    attendance = models.ForeignKey(EmployeeAttendance, on_delete=models.CASCADE, related_name="attendance_employees",
                                   null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances", null=True)
    # basic fields
    attendance_time = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=100)


class EmployeeLeaveItem(models.Model):
    STATUS = (('APPROVED', 'APPROVED'), ('UNAPPROVED', 'UNAPPROVED'), ('DECLINED', 'DECLINED'))
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="leave_employee_item", null=True)
    attendance = models.ForeignKey(EmployeeAttendance, on_delete=models.CASCADE, related_name="leave_employees",
                                   null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves", null=True)
    # basic fields
    leave_time = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=100)


class TeacherAttendanceItem(models.Model):
    STATUS = (('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT'), ('UNAPPROVED ABSENT', 'UNAPPROVED ABSENT'))
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="attendance_teacher_item", null=True)
    attendance = models.ForeignKey(StudentAttendance, on_delete=models.CASCADE, related_name="attendance_teachers",
                                   null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="attendances", null=True)
    # basic fields
    attendance_time = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=100)


class TeacherLeaveItem(models.Model):
    STATUS = (('APPROVED', 'APPROVED'), ('UNAPPROVED', 'UNAPPROVED'), ('DECLINED', 'DECLINED'))
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="leave_teacher_item", null=True)
    attendance = models.ForeignKey(StudentAttendance, on_delete=models.CASCADE, related_name="leave_teachers",
                                   null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="leaves", null=True)
    # basic fields
    leave_time = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=100)


# Session counter
class SessionCounter(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="session_counter", null=True)
    # # One of them will be occupied
    kid = models.ForeignKey(Kids, on_delete=models.DO_NOTHING, related_name="kid_sessions", null=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name="student_sessions", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_sessions", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sessions", null=True)

    # basic fields
    start_date = models.DateField()
    end_date = models.DateField()
    n_sessions = models.PositiveIntegerField()


class TeacherSessionCounter(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="teacher_session_counter", null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="sessions", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="teacher_group_sessions", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teacher_sessions", null=True)

    # basic fields
    start_date = models.DateField()
    end_date = models.DateField()
    n_sessions = models.PositiveIntegerField()
