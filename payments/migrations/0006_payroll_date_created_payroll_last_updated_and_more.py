# Generated by Django 4.1 on 2022-09-04 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_payroll_paid_payroll_pay_type_alter_payroll_employee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='date_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='uniqueId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
