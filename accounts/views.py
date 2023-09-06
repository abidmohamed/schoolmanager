from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from xhtml2pdf import pisa

from attendance.models import StudentAttendance, EmployeeAttendance, TeacherAttendanceItem
from payments.models import Payroll
from student.models import Student, Kids, Parent
from teacher.models import Teacher
from .filters import UserFilter
from .forms import UserLoginForm, UserForm
from .models import *
from django.contrib.auth.models import User, auth, Group
from random import randint
from uuid import uuid4
from django.http import HttpResponse
import os


# Create your views here.
# Anonymous required
def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = 'accounts:dashboard'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def login(request):
    context = {}
    if request.method == 'GET':
        form = UserLoginForm()
        context['form'] = form
        return render(request, 'accounts/login.html', context)

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            return redirect('accounts:group_check')
        else:
            context['form'] = form
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html', context)


@login_required
def group_check(request):
    group_name = Group.objects.all().filter(user=request.user)  # get logget user grouped name
    group_name = str(group_name[0])  # convert to string

    if "teacher" == group_name:
        # print("Hello Teacher")
        return redirect('accounts:teacher_dashboard')
    elif "student" == group_name:
        return redirect('accounts:student_dashboard')
    elif "parent" == group_name:
        return redirect('accounts:parent_dashboard')
    else:
        return redirect('accounts:dashboard')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


@login_required
def users(request):
    context = {}
    users_list = User.objects.filter(is_superuser=False).order_by('first_name')

    myFilter = UserFilter(request.GET, queryset=users_list)

    # paginate after filtering
    users_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(users_list, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['users'] = users

    # company = Settings.objects.all().filter()[:1].get()
    # context['company'] = company

    user_form = UserForm()

    groups = Group.objects.all()

    context['form'] = user_form
    context['groups'] = groups

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)

            selected_group = request.POST.get('group')
            # Remove white spaces
            selected_group = ''.join(selected_group.split())

            group = Group.objects.get(id=selected_group)
            user.save()
            user.groups.add(group)

            user.save()
            messages.success(request, 'New User Added')
            return redirect("accounts:users")
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('accounts:users')

    return render(request, "user/users.html", context)


@login_required
def dashboard(request):
    context = {}

    # Creating Groups
    if not Group.objects.all().filter(name='accountant'):
        Group.objects.create(name='accountant')
        messages.success(request, "You can create users of type Accountant")

    if not Group.objects.all().filter(name='admin'):
        Group.objects.create(name='admin')
        messages.success(request, "You can create users of type System Admin")

    if not Group.objects.all().filter(name='hr_manager'):
        Group.objects.create(name='hr_manager')
        messages.success(request, "You can create users of type HR Manager")

    if not Group.objects.all().filter(name='general_manager'):
        Group.objects.create(name='general_manager')
        messages.success(request, "You can create users of type General Manager")

    if not Group.objects.all().filter(name='management'):
        Group.objects.create(name='management')
        messages.success(request, "You can create users of type Management")

    if not Group.objects.all().filter(name='reception'):
        Group.objects.create(name='reception')
        messages.success(request, "You can create users of type Reception")

    if not Group.objects.all().filter(name='teacher'):
        Group.objects.create(name='teacher')
        messages.success(request, "You can create users of type Teacher")

    if not Group.objects.all().filter(name='parent'):
        Group.objects.create(name='parent')
        messages.success(request, "You can create users of type Parent")

    if not Group.objects.all().filter(name='student'):
        Group.objects.create(name='student')
        messages.success(request, "You can create users of type Student")

    # students activity stats
    active_students = Student.objects.filter(is_active=True).count()
    inactive_students = Student.objects.filter(is_active=False).count()
    total_students = active_students + inactive_students
    # Kids activity stats
    active_kids = Kids.objects.filter(is_active=True).count()
    inactive_kids = Kids.objects.filter(is_active=False).count()
    total_kids = active_kids + inactive_kids
    # students parents with the Most debt
    top_five_students = Student.objects.filter(debt__gt=0).order_by('-debt')[:5]
    top_five_parents = Parent.objects.filter(debt__gt=0).order_by('-debt')[:5]
    # attendance employees & students
    student_attendance = StudentAttendance.objects.filter(status=False)
    employee_attendance = EmployeeAttendance.objects.filter(status=False)
    # payroll for teachers and employees
    employees_payroll = Payroll.objects.filter(paid=False, pay_type='EMPLOYEE')
    teachers_payroll = Payroll.objects.filter(paid=False, pay_type='TEACHER')

    context['active_students'] = active_students
    context['inactive_students'] = inactive_students
    context['total_students'] = total_students
    context['active_kids'] = active_kids
    context['inactive_kids'] = inactive_kids
    context['total_kids'] = total_kids
    context['top_five_students'] = top_five_students
    context['top_five_parents'] = top_five_parents
    context['student_attendance'] = student_attendance
    context['employee_attendance'] = employee_attendance
    context['employees_payroll'] = employees_payroll
    context['teachers_payroll'] = teachers_payroll

    return render(request, 'accounts/dashboard.html', context)


@login_required
def teacher_dashboard(request):
    context = {}
    # fetch data
    try:
        teacher = Teacher.objects.get(profile=request.user)
        attendances = TeacherAttendanceItem.objects.filter(teacher=teacher).order_by("-attendance__attendance_date")[:25]
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('/')

    context['teacher'] = teacher
    context['attendances'] = attendances

    # calculate Presence
    all_sessions = 0
    present = 0
    absent = 0
    unapproved_absent = 0

    for attendance in attendances:
        all_sessions += 1
        if attendance.status == "PRESENT":
            present += 1
        elif attendance.status == "ABSENT":
            absent += 1
        else:
            unapproved_absent += 1

    context['all_sessions'] = all_sessions
    context['present'] = present
    context['absent'] = absent
    context['unapproved_absent'] = unapproved_absent

    return render(request, 'accounts/teacher_dashboard.html', context)


@login_required
def parent_dashboard(request):
    context = {}
    return render(request, 'accounts/parent_dashboard.html', context)


@login_required
def student_dashboard(request):
    context = {}
    return render(request, 'accounts/dashboard.html', context)
