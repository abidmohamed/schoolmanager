import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth, Group

# Create your views here.
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from accounts.forms import CreateUserForm
from attendance.models import TeacherLeaveItem, TeacherAttendanceItem
from payments.models import Payroll
from teacher.filters import TeacherFilter, SubjectFilter
from teacher.forms import SubjectForm, TeacherForm
from teacher.models import Subject, Teacher


# Subjects
@login_required
def subjects(request):
    context = {}

    subjects_list = Subject.objects.all().order_by('-name')

    myFilter = SubjectFilter(request.GET, queryset=subjects_list)

    # paginate after filtering
    subjects_list = myFilter.qs

    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(subjects_list, 5)

    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)

    context['subjects'] = subjects
    context['myFilter'] = myFilter

    if request.method == 'GET':
        form = SubjectForm()
        context['form'] = form
        return render(request, 'subjects/subjects.html', context)

    if request.method == 'POST':
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "New Subject Added")
            return redirect('teachers:subjects')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('teachers:subjects')

    return render(request, 'subjects/subjects.html', context)


@login_required
def subject_details(request, pk):
    context = {}
    # fetch data
    try:
        subject = Subject.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('teachers:subjects')

    context['subject'] = subject

    if request.method == 'GET':
        form = SubjectForm(instance=subject)
        context['form'] = form
        render(request, 'subjects/details.html', context)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            subject = form.save()
            subject.user = request.user
            subject.save()
            messages.success(request, 'Subject Updated')
            return redirect('teachers:subject_details', subject.id)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('teachers:subject_details', subject.id)

    return render(request, 'subjects/details.html', context)


# Teachers
@login_required
def teachers(request):
    context = {}
    teachers_list = Teacher.objects.all().order_by('-name')

    myFilter = TeacherFilter(request.GET, queryset=teachers_list)

    # paginate after filtering
    teachers_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(teachers_list, 5)

    try:
        teachers = paginator.page(page)
    except PageNotAnInteger:
        teachers = paginator.page(1)
    except EmptyPage:
        teachers = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['teachers'] = teachers

    if request.method == 'GET':
        form = TeacherForm()
        user_form = CreateUserForm()
        context['form'] = form
        context['user_form'] = user_form
        return render(request, 'teachers/teachers.html', context)

    if request.method == 'POST':
        form = TeacherForm(request.POST)
        user_form = CreateUserForm(request.POST)

        if form.is_valid() and user_form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            profile = user_form.save()

            # Filter groups by name
            teacher_group = Group.objects.get(name='teacher')
            profile.groups.add(teacher_group)

            profile.save()
            teacher.profile = profile
            teacher.save()
            messages.success(request, 'New Teacher Added')
            return redirect('teachers:teacher_details', teacher.slug)
        else:
            # Construct form errors message
            print(form.errors.as_data())
            print(user_form.errors.as_data())
            messages.error(
                request,
                'Problem processing your request '
                + str(form.errors.as_data())
                + ' '
                + str(user_form.errors.as_data())
            )
            return redirect('teachers:teachers')

    return render(request, 'teachers/teachers.html', context)


@login_required
def update_teacher(request, slug):
    pass


@login_required
def teacher_details(request, slug):
    context = {}
    # fetch data
    try:
        teacher = Teacher.objects.get(slug=slug)
        groups = teacher.teacher_groups.all()
        attendances = TeacherAttendanceItem.objects.filter(teacher=teacher).order_by("-attendance__attendance_date")[:5]
        payrolls = Payroll.objects.filter(teacher=teacher).order_by("-pay_date")[:5]

    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('teachers:teachers')

    context['teacher'] = teacher
    context['groups'] = groups
    context['attendances'] = attendances
    context['payrolls'] = payrolls

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

    if request.method == 'GET':
        form = TeacherForm(instance=teacher)
        context['form'] = form
        return render(request, 'teachers/details.html', context)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)

        if form.is_valid():
            teacher = form.save()
            teacher.user = request.user
            teacher.save()
            messages.success(request, 'Teacher Updated')
            return redirect('teachers:teacher_details', teacher.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('teachers:teacher_details', teacher.slug)

    return render(request, 'teachers/details.html', context)


@login_required
def teacher_attendances(request):
    context = {}
    # fetch data
    try:
        teacher = Teacher.objects.get(profile=request.user)
        groups = teacher.teacher_groups.all()
        attendances = TeacherAttendanceItem.objects.filter(teacher=teacher).order_by("-attendance__attendance_date")[:25]
        payrolls = Payroll.objects.filter(teacher=teacher).order_by("-pay_date")[:5]

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

    return render(request, 'teachers/attendances.html', context)


@login_required
def teacher_groups_pdf(request, slug):
    context = {}
    # fetch data
    try:
        teacher = Teacher.objects.get(slug=slug)
        groups = teacher.teacher_groups.all()
    except:
        messages.error(request, 'Something went wrong Fetching Data In group PDF')
        return redirect('teachers:teachers')

    context['teacher'] = teacher
    context['groups'] = groups

    html = render_to_string('teachers/group_pdf.html',
                            context
                            )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=table_{teacher}_{datetime.datetime.now()}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
