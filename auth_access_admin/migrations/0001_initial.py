# Generated by Django 3.0.8 on 2020-07-30 14:52

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontpage', '0002_auto_20200730_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_type', models.CharField(max_length=20, verbose_name='Place Descriptor (Road, Way, drive...)')),
                ('number', models.PositiveIntegerField(blank=True, verbose_name='Number')),
                ('place_name', models.CharField(max_length=100, verbose_name='Name of the place')),
                ('city_name', models.CharField(max_length=100, verbose_name='City Name')),
                ('postal_code', models.PositiveIntegerField(verbose_name='Postal Code')),
                ('remarks', models.CharField(max_length=200, verbose_name='Anything Else !')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=14, verbose_name='Emergency Contact Phone Number')),
                ('IdScan', models.ImageField(upload_to='ids', verbose_name='Scan of Employee ID')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('frontpage.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('familymember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='auth_access_admin.FamilyMember')),
                ('occupation', models.CharField(max_length=100, verbose_name='Employee Job Type')),
                ('employee_nr', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='Em)ployee Number')),
                ('diploma', models.CharField(max_length=100, verbose_name='Highest Field Diploma obtained')),
                ('Is_manager', models.BooleanField(verbose_name='Manager of the CC facility')),
                ('employee_contract', models.ImageField(upload_to='e_contracts', verbose_name="Scan of Employee's Work Contract")),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth_access_admin.familymember',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
