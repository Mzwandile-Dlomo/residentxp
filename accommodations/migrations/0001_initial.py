# Generated by Django 5.0.5 on 2024-05-17 08:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField(help_text='Total number of students the building can accommodate')),
                ('gender_type', models.CharField(choices=[('unisex', 'Unisex'), ('male', 'Male'), ('female', 'Female')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=3)),
                ('capacity', models.PositiveIntegerField(default=1)),
                ('room_type', models.CharField(choices=[('single', 'Single'), ('single_ensuite', 'Single Ensuite'), ('double', 'Double'), ('double_ensuite', 'Double Ensuite')], max_length=20)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='accommodations.building')),
                ('occupants', models.ManyToManyField(blank=True, related_name='rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_requests', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_requests', to='accommodations.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomInspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection_date', models.DateField(auto_now_add=True)),
                ('check_in', models.BooleanField(default=False)),
                ('check_out', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('pending', 'Pending'), ('completed', 'Completed')], default='requested', max_length=20)),
                ('inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inspections_performed', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspections_requested', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.room')),
            ],
        ),
    ]
