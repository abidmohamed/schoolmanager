from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from attendance.models import EmployeeAttendanceItem
from employee.filters import EmployeeFilter, RoleFilter
from employee.forms import EmployeeForm, RoleForm
from employee.models import Employee, Role
from payments.models import Payroll


@login_required
def employees(request):
    context = {}
    employee_list = Employee.objects.all().order_by('-name')

    myFilter = EmployeeFilter(request.GET, queryset=employee_list)

    # paginate after filtering
    employee_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(employee_list, 5)

    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['employees'] = employees

    if request.method == 'GET':
        form = EmployeeForm()
        context['form'] = form
        return render(request, 'employees/employees.html', context)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages.success(request, 'New Employee Added')
            return redirect('employees:employee_details', employee.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('employees:employees')

    return render(request, 'employees/employees.html', context)


@login_required
def employee_details(request, slug):
    context = {}
    # fetch data
    try:
        employee = Employee.objects.get(slug=slug)
        attendances = EmployeeAttendanceItem.objects.filter(employee=employee).order_by('-attendance__attendance_date')[:5]
        payrolls = Payroll.objects.filter(employee=employee).order_by('-pay_date')[:5]
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('employees:employees')

    context['employee'] = employee
    context['attendances'] = attendances
    context['payrolls'] = payrolls

    # calculate Presence
    mission = 0
    present = 0
    absent = 0
    unapproved_absent = 0

    for attendance in attendances:
        if attendance.status == "PRESENT":
            present += 1
        elif attendance.status == "ABSENT":
            absent += 1
        elif attendance.status == "MISSION":
            mission += 1
        else:
            unapproved_absent += 1

    context['mission'] = mission
    context['present'] = present
    context['absent'] = absent
    context['unapproved_absent'] = unapproved_absent

    # Handling request
    if request.method == 'GET':
        form = EmployeeForm(instance=employee)
        context['form'] = form
        return render(request, 'employees/details.html', context)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages.success(request, 'Employee Updated')
            return redirect('employees:employee_details', employee.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('employees:employee_details', employee.slug)

    return render(request, 'employees/details.html', context)


@login_required
def roles(request):
    context = {}
    roles_list = Role.objects.all().order_by('-name')

    myFilter = RoleFilter(request.GET, queryset=roles_list)

    # paginate after filtering
    roles_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(roles_list, 5)

    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['roles'] = roles

    if request.method == 'GET':
        form = RoleForm()
        context['form'] = form
        return render(request, 'roles/roles.html', context)

    if request.method == 'POST':
        form = RoleForm(request.POST)

        if form.is_valid():
            role = form.save(commit=False)
            role.user = request.user
            role.save()
            messages.success(request, 'New Role Added')
            return redirect('employees:role_details', role.id)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('employees:roles')

    return render(request, 'roles/roles.html', context)


@login_required
def role_details(request, pk):
    context = {}
    # fetch data
    try:
        role = Role.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('employees:roles')

    context['role'] = role

    if request.method == 'GET':
        form = RoleForm(instance=role)
        context['form'] = form

        return render(request, 'roles/details.html', context)

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)

        if form.is_valid():
            role = form.save(commit=False)
            role.user = request.user
            role.save()

            messages.success(request, 'Role Updated')
            return redirect('employees:role_details', role.id)

        else:
            messages.error(request, 'Problem processing your request')
            return redirect('employees:role_details', role.id)

    return render(request, 'roles/details.html', context)

