# Generated by Django 3.0.8 on 2020-08-22 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day_to_day', '0008_auto_20200822_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='desert_qtty_gr',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Quantité Déssert mangée en gr'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='starter_qtty_gr',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Quantité Entrée mangée en gr'),
        ),
        migrations.AlterField(
            model_name='medicalevent',
            name='body_temp_deg_C',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Température en °C'),
        ),
        migrations.AlterField(
            model_name='medicalevent',
            name='given_paracetamol_qtty_mg',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Paracétamol donné en MG'),
        ),
    ]