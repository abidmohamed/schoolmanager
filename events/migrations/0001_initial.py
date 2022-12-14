# Generated by Django 4.1 on 2022-08-14 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('event_type', models.CharField(choices=[('TEACHERS', 'TEACHERS'), ('MANAGEMENT', 'MANAGEMENT'), ('MEDIA', 'MEDIA'), ('TRANSPORT', 'TRANSPORT'), ('PAYMENT', 'PAYMENT')], max_length=200)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
