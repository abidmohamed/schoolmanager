# Generated by Django 4.1 on 2022-08-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_studentattendanceitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentattendanceitem',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
