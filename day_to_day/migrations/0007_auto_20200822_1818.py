# Generated by Django 3.0.8 on 2020-08-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day_to_day', '0006_auto_20200822_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='main_course_qtty_gr',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Quantité Plat de résistance mangée en gr'),
        ),
    ]