from datetime import datetime

from django.contrib.auth.models import Group
from django.db.models import Sum

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

# Create your views here.
from attendance.models import TeacherAttendanceItem, EmployeeAttendanceItem
from employee.models import Employee
from payments.filters import StudentPaymentFilter, ParentPaymentFilter, PayrollFilter
from payments.forms import StudentPaymentFrom, ParentPaymentForm
from payments.models import StudentPayment, ParentPayment, Payroll

# Students
from student.models import Parent
from teacher.models import Teacher

@login_required
def payments(request):
    context = {}
    total_value = 0
    # get all student payments (cash)
    students_payments = StudentPayment.objects.all().aggregate(Sum('amount'))
    students_payments = students_payments['amount__sum']
    # get all parent payments (cash)
    parent_payments = ParentPayment.objects.all().aggregate(Sum('amount'))
    parent_payments = parent_payments['amount__sum']
    print(Group.objects.get(user=request.user))
    if students_payments is None:
        students_payments = 0
    if parent_payments is None:
        parent_payments = 0

    total_value = (students_payments + parent_payments)
    context['students_payments'] = students_payments
    context['parent_payments'] = parent_payments
    context['total_value'] = total_value

    return render(request, "payments/payments.html", context)


@login_required
def student_payments(request):
    context = {}
    payments_list = StudentPayment.objects.all().order_by('-pay_date')

    myFilter = StudentPaymentFilter(request.GET, queryset=payments_list)

    # paginate after filtering
    payments_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(payments_list, 5)

    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['payments'] = payments

    if request.method == 'GET':
        form = StudentPaymentFrom()
        context['form'] = form
        return render(request, 'students_payments/payments.html', context)

    if request.method == 'POST':
        form = StudentPaymentFrom(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            # operate debt
            payment.student.debt -= payment.amount
            payment.student.save()
            messages.success(request, 'New Payment Added')
            return redirect('payments:student_payment_details', payment.slug)

        else:
            messages.error(request, 'Problem processing your request')
            return redirect('payments:student_payments')

    return render(request, 'students_payments/payments.html', context)


@login_required
def student_payment_details(request, slug):
    context = {}
    # fetch data
    try:
        payment = StudentPayment.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('payments:student_payments')

    context['payment'] = payment
    previous_amount = payment.amount
    previous_student = payment.student

    if request.method == 'GET':
        form = StudentPaymentFrom(instance=payment)
        context['form'] = form

        return render(request, 'students_payments/details.html', context)

    if request.method == 'POST':
        form = StudentPaymentFrom(request.POST, instance=payment)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            # handling debt
            payment.student.debt -= payment.amount
            previous_student.debt += previous_amount
            previous_student.save()
            payment.student.save()

            messages.success(request, 'Student Payment Updated')
            return redirect('payments:student_payment_details', payment.slug)

        else:
            messages.error(request, 'Problem processing your request')
            return redirect('payments:student_payment_details', payment.slug)

    return render(request, 'students_payments/details.html', context)


# Parents
@login_required
def parent_payments(request):
    context = {}
    payments_list = ParentPayment.objects.all().order_by('-pay_date')

    myFilter = ParentPaymentFilter(request.GET, queryset=payments_list)

    # paginate after filtering
    payments_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(payments_list, 5)

    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['payments'] = payments

    if request.method == 'GET':
        form = ParentPaymentForm()
        context['form'] = form
        return render(request, 'parents_payments/payments.html', context)

    if request.method == 'POST':
        form = ParentPaymentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            payment = form.save()
            payment.user = request.user
            payment.parent.debt -= payment.amount
            payment.parent.save()
            payment.save()

            messages.success(request, 'New Payment Added')
            return redirect('payments:parent_payment_details', payment.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('payments:parent_payments')

    return render(request, 'parents_payments/payments.html', context)


@login_required
def parent_payment_details(request, slug):
    context = {}
    # fetch data
    try:
        payment = ParentPayment.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('payments:parent_payments')

    context['payment'] = payment
    previous_amount = payment.amount
    previous_parent = payment.parent
    print("Previous Payment", previous_amount)

    if request.method == 'GET':
        form = ParentPaymentForm(instance=payment)
        context['form'] = form

        return render(request, 'parents_payments/details.html', context)

    if request.method == 'POST':
        form = ParentPaymentForm(request.POST, instance=payment)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            # handling debt
            # # Calculate difference in payments old & new
            payment_diff = payment.amount - previous_amount
            # apply the difference
            if payment.parent.debt < 0:
                payment.parent.debt -= payment_diff
            else:
                payment.parent.debt += payment_diff

            if previous_parent.debt < 0:
                previous_parent.debt += payment_diff
            else:
                previous_parent.debt -= payment_diff

            # print("Parent Debt after operation", payment.parent.debt)
            previous_parent.save()
            payment.parent.save()

            # print("Success")
            messages.success(request, 'Payment Updated')
            return redirect('payments:parent_payment_details', payment.slug)

        else:
            messages.error(request, 'Problem processing your request')
            return redirect('payments:parent_payment_details', payment.slug)

    return render(request, 'parents_payments/details.html', context)


@login_required
def payrolls(request):
    context = {}
    payrolls_list = Payroll.objects.all().order_by('-pay_date')

    myFilter = PayrollFilter(request.GET, queryset=payrolls_list)

    # paginate after filtering
    payrolls_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(payrolls_list, 5)

    try:
        payrolls = paginator.page(page)
    except PageNotAnInteger:
        payrolls = paginator.page(1)
    except EmptyPage:
        payrolls = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['payrolls'] = payrolls

    if not Payroll.objects.all():
        employees = Employee.objects.all().filter(is_active=True)
        teachers = Teacher.objects.all().filter(is_active=True)

        for employee in employees:
            # calculate salary
            # 1 get attendance
            attendance_present = EmployeeAttendanceItem.objects.filter(employee=employee, status='PRESENT').count()
            # 2 get salary by day and calculate
            day_salary = employee.role.salary / 26
            salary = attendance_present * day_salary
            # 3 create payroll object
            Payroll.objects.create(
                employee=employee,
                amount=salary,
                pay_date=datetime.now().date(),
                pay_type="EMPLOYEE",
            )

        for teacher in teachers:
            # calculate salary
            # 1 get attendance
            attendance_present = TeacherAttendanceItem.objects.filter(teacher=teacher, status='PRESENT').count()
            # 2 get salary by day and calculate
            day_salary = teacher.salary / 26
            salary = attendance_present * day_salary
            # 3 create payroll object
            Payroll.objects.create(
                teacher=teacher,
                amount=salary,
                pay_date=datetime.now().date(),
                pay_type="TEACHER",
            )

    return render(request, 'payrolls/payrolls.html', context)


@login_required
def payroll_details(request, slug):
    context = {}
    # fetch data
    try:
        payroll = Payroll.objects.get(slug=slug)

        if payroll.pay_type == "EMPLOYEE":
            attendances_items = EmployeeAttendanceItem.objects.filter(
                employee=payroll.employee, attendance__attendance_date__month=payroll.pay_date.month)
            daily_salary = round(payroll.employee.role.salary / 26)
        elif payroll.pay_type == "TEACHER":
            attendances_items = TeacherAttendanceItem.objects.filter(
                teacher=payroll.teacher, attendance__attendance_date__month=payroll.pay_date.month
            )
            daily_salary = round(payroll.teacher.salary / 26, 2)

    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('payments:payrolls')

    attendance_present = 0
    attendance_absent = 0
    attendance_unapproved = 0
    attendance_mission = 0

    for attendance in attendances_items:
        if attendance.status == "PRESENT":
            attendance_present += 1
        elif attendance.status == "ABSENT":
            attendance_absent += 1
        elif attendance.status == "MISSION":
            attendance_mission += 1
        else:
            attendance_unapproved += 1

    all_attendance = attendance_present + attendance_absent + attendance_unapproved
    context['payroll'] = payroll
    context['all_attendance'] = all_attendance
    context['attendance_present'] = attendance_present
    context['attendance_absent'] = attendance_absent
    context['attendance_unapproved'] = attendance_unapproved
    context['attendance_mission'] = attendance_mission
    context['daily_salary'] = daily_salary

    return render(request, 'payrolls/details.html', context)


def payroll_paid(request, slug):
    context = {}
    # fetch data
    try:
        payroll = Payroll.objects.get(slug=slug)
        payroll.paid = True
        payroll.user = request.user
        payroll.save()
        messages.success(request, "Payroll paid")
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect(request.META.get('HTTP_REFERER', 'payments:payrolls'))

    return redirect(request.META.get('HTTP_REFERER', 'payments:payrolls'))

