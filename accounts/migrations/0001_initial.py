# Generated by Django 5.0.4 on 2024-05-12 11:00

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('identification', models.CharField(max_length=15, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bursary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_information', models.CharField(blank=True, max_length=200, null=True)),
                ('reference_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RentalAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landlord', models.CharField(max_length=100)),
                ('rent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_frequency', models.CharField(choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly')], max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.user')),
                ('is_student', models.BooleanField(default=True)),
                ('student_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('application_status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('course', models.CharField(blank=True, max_length=100, null=True)),
                ('room_type', models.CharField(blank=True, max_length=50, null=True)),
                ('next_of_kin_full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('next_of_kin_address', models.CharField(blank=True, max_length=200, null=True)),
                ('next_of_kin_contact', models.CharField(blank=True, max_length=20, null=True)),
                ('next_of_kin_identification', models.CharField(blank=True, max_length=20, null=True)),
                ('bursary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='accounts.bursary')),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('paid_by_bursary', models.BooleanField(default=False)),
                ('rental_agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accounts.rentalagreement')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.user')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('groups', models.ManyToManyField(blank=True, related_name='admin_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='admin_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.user', models.Model),
        ),
        migrations.CreateModel(
            name='StudentLeader',
            fields=[
                ('student_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.student')),
                ('is_student_leader', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.student',),
        ),
        migrations.AddField(
            model_name='rentalagreement',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental_agreements', to='accounts.student'),
        ),
    ]
