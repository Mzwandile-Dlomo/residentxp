# Generated by Django 5.0.4 on 2024-05-23 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0008_alter_building_rent_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='rental_agreement',
        ),
        migrations.CreateModel(
            name='LeaseAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landlord', models.CharField(max_length=100)),
                ('rent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('semester', models.CharField(choices=[('first', 'First Semester'), ('second', 'Second Semester'), ('both', 'Both Semesters')], max_length=20)),
                ('payment_frequency', models.CharField(choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly')], max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('agreement_signed', models.BooleanField(default=False)),
                ('security_deposit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('lease_terms', models.TextField(blank=True, null=True)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lease_agreements', to='accommodations.room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lease_agreements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='lease_agreement',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accommodations.leaseagreement'),
        ),
        migrations.DeleteModel(
            name='RentalAgreement',
        ),
    ]