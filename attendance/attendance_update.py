from attendance.models import StudentAttendance, EmployeeAttendance
from group.models import Group
from datetime import datetime


def update_attendance():
    # students attendance
    groups = Group.objects.all()
    # now time
    now = datetime.today()
    for group in groups:
        attendances = group.attendance.all()
        if group.times.all():
            times = group.times.all()
            for time in times:
                # print(time)
                # print(now.date())
                # print(now.strftime("%A"))
                if time.weekday == now.strftime("%A").upper():
                    # print("FOUND ONE => ", group, " TIME : ", time.weekday)
                    if attendances.filter(attendance_date=now.date(), attendance_time=time.start_time):
                        # print("Already Exist")
                        pass
                    else:
                        # print("Created => ", group, " TIME : ", time.weekday)
                        StudentAttendance.objects.create(
                            group=group,
                            attendance_date=now.date(),
                            attendance_time=time.start_time,
                            status=False,
                        )

    # employees attendance
    if not EmployeeAttendance.objects.filter(attendance_date=now.date()):
        EmployeeAttendance.objects.create(
            attendance_date=now.date()
        )

