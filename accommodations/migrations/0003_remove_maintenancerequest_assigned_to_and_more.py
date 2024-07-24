# Generated by Django 5.0.4 on 2024-07-24 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0002_survey_closed_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenancerequest',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='maintenancerequest',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='maintenancerequest',
            name='room',
        ),
        migrations.DeleteModel(
            name='Complaint',
        ),
        migrations.DeleteModel(
            name='MaintenanceRequest',
        ),
    ]
