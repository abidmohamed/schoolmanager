# Generated by Django 4.1 on 2022-08-15 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0002_studentattendance_attendance_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentattendanceitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_attendance_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
