import datetime
from datetime import date

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
)

# Create your views here.
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from group.filters import GroupFilter
from group.forms import RoomForm, GroupForm, GroupTimeForm
from group.models import Room, Group, GroupStudent, GroupTime
from group.serializers import GroupTimeSerializer
from student.filters import KidsFilter, StudentFilter
from student.models import Kids, Student, Parent
from student.serializers import KidsSerializer
from teacher.models import Teacher


@login_required
def rooms(request):
    context = {}

    rooms = Room.objects.all().order_by('-name')
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(rooms, 25)

    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    context['rooms'] = rooms

    if request.method == 'GET':
        form = RoomForm()
        context['form'] = form
        return render(request, 'rooms/rooms.html', context)

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "New Subject Added")
            return redirect('groups:rooms')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('groups:rooms')

    return render(request, 'rooms/rooms.html', context)


# ###################### groups
@login_required
def groups(request):
    context = {}
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

    if request.method == 'GET':
        form = GroupForm()
        context['form'] = form
        return render(request, 'groups/groups.html', context)

    if request.method == 'POST':
        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            messages.success(request, 'New Group Added')
            if group.group_type == "KIDS":
                return redirect('groups:select_kids', group.slug)
            else:
                return redirect('groups:select_students', group.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('groups:groups')

    return render(request, 'groups/groups.html', context)


@login_required
def select_kids(request, slug):
    context = {}
    # fetch data
    try:
        group = Group.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('groups:groups')

    # previous kids
    previous_kids = group.items.all()

    kids_list = Kids.objects.all().order_by('-name')
    myFilter = KidsFilter(request.GET, queryset=kids_list)

    kids_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of clients in the page
    paginator = Paginator(kids_list, 25)

    try:
        kids = paginator.page(page)
    except PageNotAnInteger:
        kids = paginator.page(1)
    except EmptyPage:
        kids = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['kids'] = kids
    context['previous_kids'] = previous_kids
    context['group'] = group

    # handling request
    if request.method == 'POST':
        chosen_students = request.POST.getlist("kids")
        if len(chosen_students) != 0:
            for student_item in chosen_students:
                # saving items #student_item is id selected #group student is an item of the group
                group_student = GroupStudent()
                group_student.group = group
                group_student.user = request.user
                # removing white space
                student_item = ''.join(student_item.split())
                if group.items.all():
                    if group.items.all().filter(kid__id=student_item):
                        messages.info(request, "Student Already in this group")
                    else:
                        group_student.kid = Kids.objects.get(id=student_item)
                        group_student.save()
                else:
                    group_student.kid = Kids.objects.get(id=student_item)
                    group_student.save()

            return redirect('groups:group_details', group.slug)
        else:
            messages.error(request, "Please select at least one student")
    return render(request, 'groups/select-kids.html', context)


@login_required
def select_students(request, slug):
    context = {}
    # fetch data
    try:
        group = Group.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('groups:groups')

    # previous kids
    previous_students = group.items.all()

    students_list = Student.objects.all().order_by('-name')
    myFilter = StudentFilter(request.GET, queryset=students_list)

    students_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of clients in the page
    paginator = Paginator(students_list, 25)

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter
    context['students'] = students
    context['previous_students'] = previous_students
    context['group'] = group

    # handling request
    if request.method == 'POST':
        chosen_students = request.POST.getlist("students")
        if len(chosen_students) != 0:
            for student_item in chosen_students:
                # saving items #student_item is id selected #group student is an item of the group
                group_student = GroupStudent()
                group_student.group = group
                group_student.user = request.user
                # removing white space
                student_item = ''.join(student_item.split())
                if group.items.all():
                    if group.items.all().filter(student__id=student_item):
                        messages.info(request, "Student Already in this group")
                    else:
                        group_student.student = Student.objects.get(id=student_item)
                        group_student.save()
                else:
                    group_student.student = Student.objects.get(id=student_item)
                    group_student.save()

            return redirect('groups:group_details', group.slug)
        else:
            messages.error(request, "Please select at least one student")

    return render(request, 'groups/select-students.html', context)


@login_required
def group_details(request, slug):
    context = {}
    # Fetch data
    try:
        group = Group.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('groups:groups')

    context['group'] = group

    if request.method == 'GET':
        form = GroupForm(instance=group)
        context['form'] = form
        return render(request, 'groups/details.html', context)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            messages.success(request, 'Group Updated')
            return redirect('groups:group_details', group.slug)
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('groups:group_details', group.slug)

    return render(request, 'groups/details.html', context)


@login_required
def delete_group_item(request, id):
    context = {}
    # fetch data
    try:
        GroupStudent.objects.get(id=id).delete()
        messages.success(request, "Item Deleted")
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect(request.META.get('HTTP_REFERER', 'groups:groups'))

    return redirect(request.META.get('HTTP_REFERER', 'groups:groups'))


# ######## Times
def schedule_view():
    # List of days of the week
    days_of_week = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

    # Generate time slots separated by 2 hours
    start_time = 8  # 8:00 AM
    end_time = 20  # 8:00 PM
    step = 2

    # time_slots = [f"{str(hour).zfill(2)}:00 - {str(hour+step).zfill(2)}:00" for hour in range(start_time, end_time, step)]
    # time_slots = [(hour, hour + step) for hour in range(start_time, end_time, step)]
    time_slots = [f"{hour} - {hour + step}" for hour in range(start_time, end_time, step)]
    # context = {
    #     'days_of_week': days_of_week,
    #     'time_slots': time_slots,
    # }

    return days_of_week, time_slots


@login_required
def groups_times(request):
    context = {}

    # fetch data
    times = GroupTime.objects.all()

    context['times'] = times
    # handling requests
    if request.method == 'GET':
        form = GroupTimeForm()
        context['form'] = form
        return render(request, 'times/times.html', context)

    if request.method == 'POST':
        form = GroupTimeForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            messages.success(request, 'Group Time Added')
            return redirect('groups:groups_times')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('groups:groups_times')

    return render(request, "times/times.html", context)


@login_required
def update_groups_times(request, pk):
    context = {}
    # fetch data
    try:
        time = GroupTime.objects.get(id=pk)
        form = GroupTimeForm(instance=time)
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect('groups:groups_times')

    context['time'] = time
    context['form'] = form

    # handling request
    if request.method == 'POST':
        form = GroupTimeForm(request.POST, instance=time)

        if form.is_valid():
            time = form.save(commit=False)
            time.user = request.user
            time.save()
            messages.success(request, "Time Updated")
            return redirect('groups:groups_times')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('groups:groups_times')

    return render(request, 'times/update.html', context)


@login_required
def delete_groups_times(request, pk):
    context = {}
    # fetch data
    try:
        GroupTime.objects.get(id=pk).delete()
        messages.success(request, "Item Deleted")
    except:
        messages.error(request, 'Something went wrong Fetching Data')
        return redirect(request.META.get('HTTP_REFERER', 'groups:groups_times'))

    return redirect(request.META.get('HTTP_REFERER', 'groups:groups_times'))


@login_required
def times_pdf(request):
    context = {}
    print("pdf")
    # fetch data
    times = GroupTime.objects.all()
    context['times'] = times
    html = render_to_string('times/pdf.html',
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


@login_required
def teacher_groups(request):
    context = {}

    try:
        teacher = Teacher.objects.get(profile=request.user)
    except:
        messages.error(request, 'Problem processing your request')

    groups = Group.objects.filter(teacher=teacher).order_by('-name')

    context['groups'] = groups

    return render(request, 'groups/teacher_groups.html', context)


@login_required
def teacher_groups_times(request):
    context = {}
    try:
        teacher = Teacher.objects.get(profile=request.user)
    except:
        messages.error(request, 'Problem processing your request')

    # Retrieve all GroupTime objects for the teacher's groups
    days_of_week, time_slots = schedule_view()

    times = GroupTime.objects.filter(group__teacher=teacher)

    context['times'] = times

    context['days_of_week'] = days_of_week
    context['time_slots'] = time_slots

    return render(request, "times/teacher_times.html", context)


@login_required
def parent_kids_times(request):
    context = {}

    try:
        parent = Parent.objects.get(profile=request.user)
    except:
        messages.error(request, 'Problem processing your request')

    days_of_week, time_slots = schedule_view()
    # Retrieve the parent's kids
    parent_kids = parent.my_kids.all()

    # Retrieve group times associated with the parent's kids
    # times = GroupTime.objects.filter(group__items__kid__in=parent_kids)

    # Create a list to store kid names along with their times
    kid_times = []

    # Iterate through the group times and collect kid names and times
    # for time in times:
    #     kid_name = time.group.items.kid.name  # Access the kid's name through related fields
    #     kid_time_info = f"{kid_name}: {time.weekday} from {time.start_time} to {time.end_time}"
    #     kid_times.append(kid_time_info)
    # Create a list to store kid and their associated group times
    kid_group_times = []

    # Iterate through each kid and retrieve their group times
    for kid in parent_kids:
        print(kid)
        times = GroupTime.objects.filter(group__items__kid=kid)
        kid_group_times.append({'kid': kid, 'times': times})

    print(kid_group_times)

    context['times'] = times
    context['kid_group_times'] = kid_group_times
    context['days_of_week'] = days_of_week
    context['time_slots'] = time_slots

    return render(request, "times/parent_times.html", context)


"""
    API endpoints
    """


class ParentKidsTimesView(APIView):

    # authentication_classes = [SessionAuthentication]  # Use appropriate authentication
    permission_classes = [IsAuthenticated]  # Use appropriate permissions

    def get(self, request):
        context = {}

        try:
            parent = get_object_or_404(Parent, profile=request.user)
        except Parent.DoesNotExist:
            return Response({'detail': 'Problem processing your request'}, status=status.HTTP_400_BAD_REQUEST)

        days_of_week, time_slots = schedule_view()

        # Retrieve the parent's kids
        parent_kids = parent.my_kids.all()

        # Create a list to store kid names along with their times
        kid_times = []

        # Create a list to store kid and their associated group times
        kid_group_times = []

        # Iterate through each kid and retrieve their group times
        for kid in parent_kids:
            times = GroupTime.objects.filter(group__items__kid=kid)
            kid_group_times.append({'kid': KidsSerializer(kid).data, 'times': GroupTimeSerializer(times, many=True).data})

        context['kid_group_times'] = kid_group_times
        context['days_of_week'] = days_of_week
        context['time_slots'] = time_slots

        return Response(context)
