from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.urls import reverse

from attendance.filters import EmployeeAttendanceFilter, TeacherAttendanceFilter, StudentAttendanceFilter, \
    EmployeeAttendanceItemFilter
from attendance.forms import StudentAttendanceForm, EmployeeAttendanceForm
from attendance.models import StudentAttendance, StudentAttendanceItem, EmployeeAttendance, EmployeeAttendanceItem, \
    EmployeeLeaveItem, TeacherAttendanceItem, TeacherLeaveItem, SessionCounter, TeacherSessionCounter
from employee.models import Employee
from group.filters import GroupFilter
from group.models import Group, GroupTime
from datetime import datetime

from student.models import Student, Kids
from teacher.models import Teacher


@login_required
def attendance_stats(request):
    context = {}
    # # show only specific groups of today
    now = datetime.today()
    times = GroupTime.objects.filter(weekday=now.strftime("%A").upper())
    # print(times)
    groups_list = Group.objects.none()
    students = Student.objects.none()
    kids = Kids.objects.none()
    current_attendances = StudentAttendance.objects.none()
    for time in times:
        if Group.objects.filter(slug=time.group.slug):
            # print(Group.objects.filter(slug=time.group.slug))
            # getting all students list
            groups_list |= Group.objects.filter(slug=time.group.slug)
            for group in groups_list:
                if group.group_type == "ADULTS":
                    students |= group.items.all().filter(student__is_active=True)
                else:
                    kids |= group.items.all().filter(kid__is_active=True)

        # present & absent students list
        current_attendances |= time.group.attendance.filter(attendance_date=now.date())

    context['groups'] = groups_list
    context['students'] = students
    context['kids'] = kids
    context['current_attendances'] = current_attendances

    return render(request, 'attendances/stats.html', context)


@login_required
def attendances(request):
    context = {}
    # fetch data
    now = datetime.today()

    # # calculate All today students
    times = GroupTime.objects.filter(weekday=now.strftime("%A").upper())
    current_groups = Group.objects.none()
    total_students = 0
    present_students = 0
    absent_students = 0
    for time in times:
        # all students
        total_students += time.group.items.all().count()
        # present & absent students
        current_attendances = time.group.attendance.filter(attendance_date=now.date())
        for attendance in current_attendances:
            for student_attendance in attendance.attendance_students.all():
                if student_attendance.status:
                    present_students += 1
                else:
                    absent_students += 1

    groups_list = Group.objects.all().order_by('-name')

    myFilter = GroupFilter(request.GET, queryset=groups_list)

    # paginate after filtering
    groups_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(groups_list, 25)

    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['groups'] = groups
    context['total_students'] = total_students
    context['present_students'] = present_students
    context['absent_students'] = absent_students

    return render(request, 'attendances/groups.html', context)


@login_required
def group_attendances(request, slug):
    context = {}
    # time variables
    # fetch data
    try:
        group = Group.objects.get(slug=slug)
        attendances = group.attendance.all().order_by('-attendance_date')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('attendances:attendances')

    context['group'] = group
    context['attendances'] = attendances

    if group.times.all():
        times = group.times.all()
        for time in times:
            # print(time)
            now = datetime.today()
            # print(now.date())
            # print(now.strftime("%A"))
            if time.weekday == now.strftime("%A").upper():
                if attendances.filter(attendance_date=now.date(), attendance_time=time.start_time):
                    # print("Exist")
                    pass
                else:
                    StudentAttendance.objects.create(
                        user=request.user,
                        group=group,
                        attendance_date=now.date(),
                        attendance_time=time.start_time,
                        status=False,
                    )

    if request.method == 'GET':
        form = StudentAttendanceForm()
        context['form'] = form
        return render(request, 'attendances/group_attendances.html', context)

    if request.method == 'POST':
        form = StudentAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            # check if attendance exists
            # print(attendance.attendance_date)
            if StudentAttendance.objects.filter(group=group, attendance_date=attendance.attendance_date):
                messages.error(request, "Attendance already exists in the same date")
                return redirect("attendances:group_attendances", group.slug)
            else:
                StudentAttendance.objects.create(
                    user=request.user,
                    group=group,
                    attendance_date=attendance.attendance_date,
                    attendance_time=attendance.attendance_time,
                    status=False,
                )
                messages.success(request, "Attendance created")

                return redirect("attendances:group_attendances", group.slug)

    return render(request, 'attendances/group_attendances.html', context)


@login_required
def students_attendances(request, slug):
    context = {}
    # fetch data
    try:
        attendance = StudentAttendance.objects.get(slug=slug)
        group = Group.objects.get(slug=attendance.group.slug)
        if group.group_type == "ADULTS":
            students = group.items.all().filter(student__is_active=True)
        else:
            students = group.items.all().filter(kid__is_active=True)

        teacher = Teacher.objects.get(slug=group.teacher.slug)
    except:
        messages.error(request, 'Something went wrong In Students Attendance')
        return redirect('attendances:attendances')

    print(students)
    context['group'] = group
    context['students'] = students
    context['attendance'] = attendance
    context['teacher'] = teacher

    return render(request, "attendances/students.html", context)


@login_required
def students_confirm_attendance(request, slug):
    context = {}
    # fetch data
    try:
        attendance = StudentAttendance.objects.get(slug=slug)
        group = Group.objects.get(slug=attendance.group.slug)
        if group.group_type == "ADULTS":
            students = group.items.all().filter(student__is_active=True)
        else:
            students = group.items.all().filter(kid__is_active=True)

        teacher = Teacher.objects.get(slug=group.teacher.slug)
    except:
        messages.error(request, 'Something went wrong in Confirmation')
        return redirect('attendances:attendances')

    # handling teacher
    teacher_status = request.POST[teacher.name]
    time = request.POST.get(str(teacher.id))

    if not time == "":
        time = datetime.strptime(time, '%H:%M').time()
    else:
        time = None

    if teacher_status == "PRESENT":
        teacher_status = "PRESENT"
    elif teacher_status == "ABSENT":
        teacher_status = "ABSENT"
    else:
        teacher_status = "UNAPPROVED ABSENT"

    try:
        t = TeacherAttendanceItem.objects.get(attendance=attendance, teacher=teacher)
        t.status = teacher_status
        t.attendance_time = time
        t.save()
    except TeacherAttendanceItem.DoesNotExist:
        t = TeacherAttendanceItem(user=request.user, attendance=attendance, teacher=teacher,
                                  attendance_time=time, status=teacher_status)
        t.save()
        # treating session counter
        if not TeacherSessionCounter.objects.filter(teacher=teacher, group=group, subject=group.subject):
            TeacherSessionCounter.objects.create(
                user=request.user,
                teacher=teacher,
                group=group,
                subject=group.subject,
                start_date=datetime.today().date(),
                end_date=datetime.today().date(),
                n_sessions=1
            )
        else:
            sessions = TeacherSessionCounter.filter(teacher=teacher, group=group, subject=group.subject)
            new_counter = 0
            for session in sessions:
                if session.n_sessions < group.subject.n_sessions:
                    session.n_sessions += 1
                    session.end_date = datetime.today().date()
                    session.save()
                    new_counter = 0
                    break
                else:
                    new_counter = 1

            if new_counter == 1:
                TeacherSessionCounter.objects.create(
                    user=request.user,
                    teacher=teacher,
                    group=group,
                    subject=group.subject,
                    start_date=datetime.today().date(),
                    end_date=datetime.today().date(),
                    n_sessions=1
                )

    # handling students
    for student in students:
        # if the group type adult
        print(student)
        print(group.group_type)
        if group.group_type == "ADULTS":

            status = request.POST[student.student.name]
            print(student.student.name)
            # set student status
            if status == 'present':
                status = True
            else:
                status = False

            # checking Attendance status marked before or not
            if attendance.status:
                print(attendance.status)
                try:
                    a = StudentAttendanceItem.objects.get(attendance=attendance, student=student.student)
                    a.status = status
                    a.save()
                except StudentAttendanceItem.DoesNotExist:
                    a = StudentAttendanceItem(user=request.user, attendance=attendance, student=student.student,
                                              status=status)
                    a.save()

                    # Treating sessions counter
                    if not SessionCounter.objects.filter(student=student.student, group=group, subject=group.subject):
                        SessionCounter.objects.create(
                            user=request.user,
                            student=student.student,
                            group=group,
                            subject=group.subject,
                            start_date=datetime.today().date(),
                            end_date=datetime.today().date(),
                            n_sessions=1
                        )
                    else:
                        sessions = SessionCounter.objects.filter(student=student.student, group=group,
                                                                 subject=group.subject)
                        new_counter = 0
                        for session in sessions:
                            if session.n_sessions < group.subject.n_sessions:
                                session.n_sessions += 1
                                session.end_date = datetime.today().date()
                                session.save()
                                new_counter = 0
                                break
                            else:
                                new_counter = 1

                        if new_counter == 1:
                            SessionCounter.objects.create(
                                user=request.user,
                                student=student.student,
                                group=group,
                                subject=group.subject,
                                start_date=datetime.today().date(),
                                end_date=datetime.today().date(),
                                n_sessions=1
                            )
                    # treating debt
                    # session price
                    session_price = group.subject.price / group.subject.n_sessions

                    # print("SESSION PRICE ==> ", session_price)
                    student.student.debt += session_price
                    student.student.save()

            else:
                a = StudentAttendanceItem(user=request.user, attendance=attendance, student=student.student,
                                          status=status)
                a.save()
                attendance.status = True
                attendance.save()

                # Treating sessions counter
                if not SessionCounter.objects.filter(student=student.student, group=group, subject=group.subject):
                    SessionCounter.objects.create(
                        user=request.user,
                        student=student.student,
                        group=group,
                        subject=group.subject,
                        start_date=datetime.today().date(),
                        end_date=datetime.today().date(),
                        n_sessions=1
                    )
                else:
                    sessions = SessionCounter.objects.filter(student=student.student, group=group,
                                                             subject=group.subject)
                    new_counter = 0
                    for session in sessions:
                        if session.n_sessions < group.subject.n_sessions:
                            session.n_sessions += 1
                            session.end_date = datetime.today().date()
                            session.save()
                            new_counter = 0
                            break
                        else:
                            new_counter = 1

                    if new_counter == 1:
                        SessionCounter.objects.create(
                            user=request.user,
                            student=student.student,
                            group=group,
                            subject=group.subject,
                            start_date=datetime.today().date(),
                            end_date=datetime.today().date(),
                            n_sessions=1
                        )
                # treating debt
                # session price
                session_price = group.subject.price / group.subject.n_sessions

                # print("SESSION PRICE ==> ", session_price)
                student.student.debt += session_price
                student.student.save()


        else:
            # if the group type kids

            post_status = request.POST[student.kid.name]
            print(student.kid.name)
            # set student status
            if post_status == 'present':
                status = True
            else:
                status = False

            # checking Attendance status marked before or not
            if attendance.status:
                print(attendance.status)
                try:
                    a = StudentAttendanceItem.objects.get(attendance=attendance, kid=student.kid)
                    a.status = status
                    a.save()
                except StudentAttendanceItem.DoesNotExist:
                    a = StudentAttendanceItem(user=request.user, attendance=attendance, kid=student.kid,
                                              status=status)
                    a.save()

                    # Treating sessions counter
                    if not SessionCounter.objects.filter(kid=student.kid, group=group, subject=group.subject):
                        SessionCounter.objects.create(
                            user=request.user,
                            kid=student.kid,
                            group=group,
                            subject=group.subject,
                            start_date=datetime.today().date(),
                            end_date=datetime.today().date(),
                            n_sessions=1
                        )
                    else:
                        sessions = SessionCounter.objects.filter(kid=student.kid, group=group, subject=group.subject)
                        new_counter = 0
                        for session in sessions:
                            if session.n_sessions < group.subject.n_sessions:
                                session.n_sessions += 1
                                session.end_date = datetime.today().date()
                                session.save()
                                new_counter = 0
                                break
                            else:
                                new_counter = 1

                        if new_counter == 1:
                            SessionCounter.objects.create(
                                user=request.user,
                                kid=student.kid,
                                group=group,
                                subject=group.subject,
                                start_date=datetime.today().date(),
                                end_date=datetime.today().date(),
                                n_sessions=1
                            )

                    # treating debt
                    # session price
                    session_price = group.subject.price / group.subject.n_sessions
                    student.kid.parent.debt += session_price
                    student.kid.parent.save()

            else:
                # print("NEWWW VALUE 2222")
                a = StudentAttendanceItem(user=request.user, attendance=attendance, kid=student.kid,
                                          status=status)
                a.save()
                attendance.status = True
                attendance.save()
                # Treating sessions counter
                if not SessionCounter.objects.filter(kid=student.kid, group=group, subject=group.subject):
                    SessionCounter.objects.create(
                        user=request.user,
                        kid=student.kid,
                        group=group,
                        subject=group.subject,
                        start_date=datetime.today().date(),
                        end_date=datetime.today().date(),
                        n_sessions=1
                    )
                else:
                    sessions = SessionCounter.objects.filter(kid=student.kid, group=group, subject=group.subject)
                    new_counter = 0
                    for session in sessions:
                        if session.n_sessions < group.subject.n_sessions:
                            session.n_sessions += 1
                            session.end_date = datetime.today().date()
                            session.save()
                            new_counter = 0
                            break
                        else:
                            new_counter = 1

                    if new_counter == 1:
                        SessionCounter.objects.create(
                            user=request.user,
                            kid=student.kid,
                            group=group,
                            subject=group.subject,
                            start_date=datetime.today().date(),
                            end_date=datetime.today().date(),
                            n_sessions=1
                        )

                    # treating debt
                    # session price
                    session_price = group.subject.price / group.subject.n_sessions
                    student.kid.parent.debt += session_price
                    student.kid.parent.save()

    return HttpResponseRedirect(reverse("attendances:group_attendances", args=(group.slug,)))


@login_required
def students_attendances_details(request, slug):
    context = {}
    # fetch data
    try:
        attendance = StudentAttendance.objects.get(slug=slug)
        group = Group.objects.get(slug=attendance.group.slug)
        students = StudentAttendanceItem.objects.filter(attendance=attendance)
        teacher = Teacher.objects.get(slug=group.teacher.slug)

        if TeacherAttendanceItem.objects.filter(teacher=teacher, attendance=attendance):
            teacher_attendance = TeacherAttendanceItem.objects.get(teacher=teacher, attendance=attendance)
        else:
            teacher_attendance = None

        if TeacherLeaveItem.objects.filter(teacher=teacher, attendance=attendance):
            teacher_leaving = TeacherLeaveItem.objects.get(teacher=teacher, attendance=attendance)
        else:
            teacher_leaving = None
    except:
        messages.error(request, 'Something went wrong')
        return redirect('attendances:attendances')

    context['group'] = group
    context['students'] = students
    context['teacher'] = teacher
    context['attendance'] = attendance
    context['teacher_attendance'] = teacher_attendance
    context['teacher_leaving'] = teacher_leaving
    # for student in students:
    #    print(student.status)

    return render(request, "attendances/students_details.html", context)


@login_required
def employee_attendances(request):
    now = datetime.today()
    # check if attendance created
    if not EmployeeAttendance.objects.filter(attendance_date=now.date()):
        EmployeeAttendance.objects.create(
            user=request.user,
            attendance_date=now.date()
        )

    context = {}
    # fetch data
    attendances_list = EmployeeAttendance.objects.all().order_by('-attendance_date')

    myFilter = EmployeeAttendanceFilter(request.GET, queryset=attendances_list)

    # paginate after filtering
    attendances_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(attendances_list, 25)

    try:
        attendances = paginator.page(page)
    except PageNotAnInteger:
        attendances = paginator.page(1)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['attendances'] = attendances

    if request.method == 'GET':
        form = EmployeeAttendanceForm()
        context['form'] = form
        return render(request, 'attendance_employees/attendances.html', context)

    if request.method == 'POST':
        form = EmployeeAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            # check if attendance exists
            if EmployeeAttendance.objects.filter(attendance_date=attendance.attendance_date):
                messages.error(request, "Attendance already exists in the same date")
                return redirect("attendances:employee_attendances")
            else:
                EmployeeAttendance.objects.create(
                    user=request.user,
                    attendance_date=attendance.attendance_date
                )
                messages.success(request, "Attendance created")

                return redirect("attendances:employee_attendances")

    return render(request, 'attendance_employees/attendances.html', context)


@login_required
def employee_list_attendance(request, slug):
    context = {}

    # fetch data
    try:
        attendance = EmployeeAttendance.objects.get(slug=slug)
        employees = Employee.objects.all()
    except:
        messages.error(request, 'Something went wrong In Employee List')
        return redirect('attendances:employee_attendances')

    context['employees'] = employees
    context['attendance'] = attendance

    return render(request, "attendance_employees/employees.html", context)


@login_required
def employees_confirm_attendance(request, slug):
    context = {}
    # fetch data
    try:
        attendance = EmployeeAttendance.objects.get(slug=slug)
        employees = Employee.objects.all()

    except:
        messages.error(request, 'Something went wrong in Confirmation')
        return redirect('attendances:employee_list_attendance', slug)

    for employee in employees:
        # print(request.POST)
        # print(request.POST.get(str(employee.id)))
        status = request.POST[employee.name]
        time = request.POST.get(str(employee.id))
        if not time == "":
            time = datetime.strptime(time, '%H:%M').time()
        else:
            time = None

        if status == 'PRESENT':
            status = 'PRESENT'
        elif status == 'ABSENT':
            status = 'ABSENT'
        elif status == 'UNAPPROVED ABSENT':
            status = 'UNAPPROVED ABSENT'
        else:
            status = 'MISSION'

        if attendance.status:
            try:
                e = EmployeeAttendanceItem.objects.get(attendance=attendance, employee=employee)
                e.attendance_time = time
                e.status = status
                e.save()
                attendance.user = request.user
                attendance.save()
            except EmployeeAttendanceItem.DoesNotExist:
                e = EmployeeAttendanceItem(user=request.user, attendance=attendance, employee=employee,
                                           attendance_time=time, status=status)
                e.save()
                attendance.user = request.user
                attendance.save()
        else:
            e = EmployeeAttendanceItem(user=request.user, attendance=attendance, employee=employee,
                                       attendance_time=time, status=status)
            e.save()
            attendance.status = True
            attendance.user = request.user
            attendance.save()

    return HttpResponseRedirect(reverse("attendances:employee_attendances"))


@login_required
def employees_attendance_details(request, slug):
    context = {}
    # fetch data
    try:
        attendance = EmployeeAttendance.objects.get(slug=slug)
        employees = EmployeeAttendanceItem.objects.filter(attendance=attendance)
        employees_leave = EmployeeLeaveItem.objects.filter(attendance=attendance)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('attendances:employee_attendances')

    context['attendance'] = attendance
    context['employees'] = employees
    context['employees_leave'] = employees_leave

    return render(request, "attendance_employees/details.html", context)


@login_required
def employee_list_leave(request, slug):
    context = {}

    # fetch data
    try:
        attendance = EmployeeAttendance.objects.get(slug=slug)
        # employees = Employee.objects.all()
        employees = attendance.attendance_employees.filter(status="PRESENT")
    except:
        messages.error(request, 'Something went wrong In employee list leave')
        return redirect('attendances:employee_attendances')

    context['employees'] = employees
    context['attendance'] = attendance

    return render(request, "attendance_employees/employees_leave.html", context)


@login_required
def employees_confirm_leave(request, slug):
    context = {}
    # fetch data
    try:
        attendance = EmployeeAttendance.objects.get(slug=slug)
        # employees = Employee.objects.all()
        employees = attendance.attendance_employees.filter(status="PRESENT")
    except:
        messages.error(request, 'Something went wrong In employee leave confirmation')
        return redirect('attendances:employee_attendances')

    for item in employees:
        status = request.POST[item.employee.name]
        # print(status)
        time = request.POST.get(str(item.employee.id))
        if not time == "":
            time = datetime.strptime(time, '%H:%M').time()
        else:
            time = None

        if status == 'APPROVED':
            status = 'APPROVED'
        elif status == 'UNAPPROVED':
            status = 'UNAPPROVED'
        else:
            status = 'DECLINED'

        try:
            e = EmployeeLeaveItem.objects.get(attendance=attendance, employee=item.employee)
            e.status = status
            e.save()
            attendance.user = request.user
            attendance.save()
        except EmployeeLeaveItem.DoesNotExist:
            e = EmployeeLeaveItem(user=request.user, attendance=attendance, employee=item.employee,
                                  leave_time=time, status=status)
            e.save()
            attendance.user = request.user
            attendance.save()

    return HttpResponseRedirect(reverse("attendances:employee_attendances"))


@login_required
def teacher_leave(request, slug):
    context = {}
    # fetch data
    try:
        attendance = StudentAttendance.objects.get(slug=slug)
        group = Group.objects.get(slug=attendance.group.slug)
        students = group.items.all()
        teacher = Teacher.objects.get(slug=group.teacher.slug)
        if TeacherAttendanceItem.objects.filter(teacher=teacher, attendance=attendance):
            teacher_attendance = TeacherAttendanceItem.objects.get(teacher=teacher, attendance=attendance)
        else:
            teacher_attendance = None
    except:
        messages.error(request, 'Something went wrong In teacher Leave')
        return redirect('attendances:attendances')

    context['group'] = group
    context['students'] = students
    context['attendance'] = attendance
    context['teacher'] = teacher
    context['teacher_attendance'] = teacher_attendance

    return render(request, "attendances/leave.html", context)


@login_required
def teacher_confirm_leave(request, slug):
    context = {}
    # fetch data
    try:
        attendance = StudentAttendance.objects.get(slug=slug)
        group = Group.objects.get(slug=attendance.group.slug)
        students = group.items.all()
        teacher = Teacher.objects.get(slug=group.teacher.slug)
    except:
        messages.error(request, 'Something went wrong In group Attendance')
        return redirect('attendances:attendances')

    status = request.POST[teacher.name]
    # print(status)
    time = request.POST.get(str(teacher.id))
    if not time == "":
        time = datetime.strptime(time, '%H:%M').time()
    else:
        time = None

    if status == 'APPROVED':
        status = 'APPROVED'
    elif status == 'UNAPPROVED':
        status = 'UNAPPROVED'
    else:
        status = 'DECLINED'

    try:
        t = TeacherLeaveItem.objects.get(attendance=attendance, teacher=teacher)
        t.status = status
        t.save()
        attendance.user = request.user
        attendance.save()
    except TeacherLeaveItem.DoesNotExist:
        t = TeacherLeaveItem(user=request.user, attendance=attendance,
                             teacher=teacher, leave_time=time, status=status)
        t.save()
        attendance.user = request.user
        attendance.save()

    return HttpResponseRedirect(reverse("attendances:attendances"))


@login_required
def attendances_details(request, slug, item):
    context = {}
    try:
        if item == "1":
            # teacher
            attendance_item = Teacher.objects.get(slug=slug)
            attendances_list = TeacherAttendanceItem.objects.filter(teacher=attendance_item).order_by(
                "-attendance__attendance_date")

            myFilter = TeacherAttendanceFilter(request.GET, queryset=attendances_list)

        elif item == "2":
            # Student
            attendance_item = Student.objects.get(slug=slug)
            attendances_list = StudentAttendanceItem.objects.filter(student=attendance_item).order_by(
                "-attendance__attendance_date")

            myFilter = StudentAttendanceFilter(request.GET, queryset=attendances_list)

        elif item == "3":
            # kids
            attendance_item = Kids.objects.get(slug=slug)
            attendances_list = StudentAttendanceItem.objects.filter(kid=attendance_item).order_by(
                "-attendance__attendance_date")

            myFilter = StudentAttendanceFilter(request.GET, queryset=attendances_list)

        else:
            # employee
            attendance_item = Employee.objects.get(slug=slug)
            attendances_list = EmployeeAttendanceItem.objects.filter(employee=attendance_item).order_by(
                "-attendance__attendance_date")
            myFilter = EmployeeAttendanceItemFilter(request.GET, queryset=attendances_list)

    except:
        messages.error(request, 'Something went wrong In Attendance Details')
        return redirect('attendances:attendances')

    # paginate after filtering
    attendances_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(attendances_list, 25)

    try:
        attendances = paginator.page(page)
    except PageNotAnInteger:
        attendances = paginator.page(1)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    context['attendance_item'] = attendance_item
    context['attendances'] = attendances
    context['myFilter'] = myFilter

    return render(request, 'attendances/attendances.html', context)
