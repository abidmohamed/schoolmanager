# Generated by Django 4.1 on 2022-08-30 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_kids_is_active_student_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='kids',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
