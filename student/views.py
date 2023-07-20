import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from attendance.models import SessionCounter
from group.models import GroupTime
from payments.models import StudentPayment, ParentPayment
from student.filters import ParentFilter, KidsFilter, StudentFilter
from student.forms import ParentForm, KidsForm, StudentForm
from student.models import Parent, Kids, Student


@login_required
def parents(request):
    context = {}
    parents_list = Parent.objects.all().order_by('-name')

    myFilter = ParentFilter(request.GET, queryset=parents_list)

    # paginate after filtering
    parents_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(parents_list, 5)

    try:
        parents = paginator.page(page)
    except PageNotAnInteger:
        parents = paginator.page(1)
    except EmptyPage:
        parents = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['parents'] = parents

    if request.method == 'GET':
        form = ParentForm()
        context['form'] = form
        return render(request, 'parent/parents.html', context)

    if request.method == 'POST':
        form = ParentForm(request.POST)

        if form.is_valid():
            parent = form.save(commit=False)
            parent.user = request.user
            parent.save()
            messages.success(request, 'New Parent Added')
            return redirect('students:parent_details', parent.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('students:parents')

    return render(request, 'parent/parents.html', context)


@login_required
def update_parent(request, slug):
    # fetch data
    try:
        parent = Parent.objects.get(slug=slug)
        form = ParentForm(instance=parent)
    except:
        messages.error(request, 'Something went wrong When Fetching Data')
        return redirect('students:parents')

    context = {}
    # company = Settings.objects.all().filter()[:1].get()
    # context['company'] = company
    context['parent'] = parent
    context['form'] = form

    # handling request
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)

        if form.is_valid():
            parent = form.save()
            messages.success(request, 'Parent Updated')
            return redirect('students:parent_details', parent.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('students:parents')

    return render(request, 'parent/update.html', context)


@login_required
def parent_details(request, slug):
    context = {}
    # fetch data
    try:
        parent = Parent.objects.get(slug=slug)
        kids = parent.my_kids.all()
        # Payments
        payments = ParentPayment.objects.filter(parent=parent).order_by('-pay_date')[:5]
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('students:parents')
    context['parent'] = parent
    context['kids'] = kids
    context['payments'] = payments

    # Handling request
    if request.method == 'GET':
        form = KidsForm()
        context['form'] = form
        return render(request, 'parent/details.html', context)

    if request.method == 'POST':
        form = KidsForm(request.POST)
        if form.is_valid():
            kid = form.save(commit=False)
            kid.user = request.user
            kid.parent = parent
            kid.save()
            messages.success(request, 'New Kid Added')
            return redirect('students:parent_details', parent.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('students:parent_details', parent.slug)

    return render(request, 'parent/details.html', context)


@login_required
def kids(request):
    context = {}
    # fetch data
    kids_list = Kids.objects.all().order_by('-name')

    myFilter = KidsFilter(request.GET, queryset=kids_list)

    # paginate after filtering
    kids_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(kids_list, 5)
    try:
        kids = paginator.page(page)
    except PageNotAnInteger:
        kids = paginator.page(1)
    except EmptyPage:
        kids = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['kids'] = kids

    if request.method == 'GET':
        form = KidsForm()
        context['form'] = form
        return render(request, 'kids/kids.html', context)

    return render(request, 'kids/kids.html', context)


@login_required
def kid_details(request, slug):
    context = {}
    # fetch data
    try:
        kid = Kids.objects.get(slug=slug)
        # groups
        groups = kid.kid_group.all()
        # attendances
        attendances = kid.kid_attendance.all().order_by('-attendance__attendance_date')[:5]
        sessions = kid.kid_sessions.all()[:5]
        # Payments
        payments = ParentPayment.objects.filter(parent=kid.parent).order_by('-pay_date')[:5]
    except:
        messages.error(request, 'Something went wrong Fetching Data In Details')
        return redirect('students:kids')

    context['kid'] = kid
    context['groups'] = groups
    context['attendances'] = attendances
    context['sessions'] = sessions
    context['payments'] = payments

    # calculate Presence
    all_sessions = 0
    present = 0
    absent = 0
    for attendance in attendances:
        all_sessions += 1
        if attendance.status:
            present += 1
        else:
            absent += 1

    context['all_sessions'] = all_sessions
    context['present'] = present
    context['absent'] = absent

    if request.method == 'GET':
        form = KidsForm(instance=kid)
        context['form'] = form

        return render(request, 'kids/details.html', context)

    if request.method == 'POST':
        form = KidsForm(request.POST, instance=kid)

        if form.is_valid():
            kid = form.save()
            messages.success(request, 'Kid Updated')
            return redirect('students:kid_details', kid.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('students:kid_details', kid.slug)

    # context['payments'] = payments
    #    print(order)
    # Handling request

    return render(request, 'kids/details.html', context)


def kid_groups_pdf(request, slug):
    context = {}
    try:
        kid = Kids.objects.get(slug=slug)
        # groups
        groups = kid.kid_group.all()

    except:
        messages.error(request, 'Something went wrong Fetching Data In Group PDF')
        return redirect('students:kids')

    context['kid'] = kid
    context['groups'] = groups

    html = render_to_string('kids/group_pdf.html',
                            context
                            )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=table_{kid}_{datetime.datetime.now()}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def kid_update(request, slug):
    context = {}
    # fetch data
    try:
        kid = Kids.objects.get(slug=slug)
        form = KidsForm(instance=kid)
        # Payments
        # payments = SellOrderPayment.objects.filter(order=order)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('students:kid_details', slug)

    context['kid'] = kid
    print(kid)
    return HttpResponse(form)


# Students
@login_required
def students(request):
    context = {}
    students_list = Student.objects.all().order_by('name')
    myFilter = StudentFilter(request.GET, queryset=students_list)

    # paginate after filtering
    students_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(students_list, 5)

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['students'] = students

    if request.method == 'GET':
        form = StudentForm()
        context['form'] = form
        return render(request, 'students/students.html', context)

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, 'New Student Added')
            return redirect('students:student_details', student.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('students:students')

    return render(request, 'students/students.html', context)


@login_required
def update_student(request, slug):
    pass


@login_required
def student_details(request, slug):
    context = {}
    # fetch data
    try:
        student = Student.objects.get(slug=slug)
        # groups
        groups = student.student_group.all()
        # attendances
        attendances = student.student_attendance.all().order_by('-attendance__attendance_date')[:5]
        sessions = student.student_sessions.all().order_by('-end_date')[:5]
        # Payments
        payments = StudentPayment.objects.filter(student=student)
    except:
        messages.error(request, 'Something went wrong Fetching Data In Details')
        return redirect('students:students')
    context['student'] = student
    context['groups'] = groups
    context['attendances'] = attendances
    context['sessions'] = sessions
    context['payments'] = payments

    # calculate Presence
    all_sessions = 0
    present = 0
    absent = 0
    for attendance in attendances:
        all_sessions += 1
        if attendance.status:
            present += 1
        else:
            absent += 1

    context['all_sessions'] = all_sessions
    context['present'] = present
    context['absent'] = absent

    if request.method == 'GET':
        form = StudentForm(instance=student)
        context['form'] = form

        return render(request, 'students/details.html', context)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, 'Student Updated')
            return redirect('students:student_details', student.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('students:student_details', student.slug)

    # context['payments'] = payments
    #    print(order)
    # Handling request

    return render(request, 'students/details.html', context)


@login_required
def groups_pdf(request, slug):
    context = {}
    # fetch data
    try:
        student = Student.objects.get(slug=slug)
        # groups
        groups = student.student_group.all()
        # attendances
        attendances = student.student_attendance.all()
        sessions = student.student_sessions.all()
        # Payments
        # payments = SellOrderPayment.objects.filter(order=order)
    except:
        messages.error(request, 'Something went wrong Fetching Data In Group PDF')
        return redirect('students:students')
    context['student'] = student
    context['groups'] = groups

    html = render_to_string('students/group_pdf.html',
                            context
                            )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=table_{student}_{datetime.datetime.now()}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def transportation_list(request):
    context = {}

    # fetch data
    try:
        times = GroupTime.objects.all()
    except:
        messages.error(request, 'Something went wrong Fetching Data In Group PDF')
        return redirect('students:students')

    context['times'] = times

    return render(request, 'transportation/times.html', context)


@login_required
def transportation_pdf(request):
    context = {}
    print("pdf")
    # fetch data
    times = GroupTime.objects.all()
    context['times'] = times
    html = render_to_string('transportation/pdf.html',
                            {
                                'times': times,
                            }
                            )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=table_{datetime.datetime.now()}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
