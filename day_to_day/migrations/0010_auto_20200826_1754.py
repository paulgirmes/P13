# Generated by Django 3.0.8 on 2020-08-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day_to_day', '0009_auto_20200822_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalevent',
            name='paracetamol_given_time',
            field=models.TimeField(blank=True, default="00:00", verbose_name="Heure d'administration"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dailyfact',
            name='time_stamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Horodatage'),
        ),
    ]
