# Generated by Django 3.0.8 on 2020-08-11 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_access_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='familymember',
            name='address',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth_access_admin.Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='city_name',
            field=models.CharField(max_length=100, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='address',
            name='number',
            field=models.PositiveIntegerField(blank=True, verbose_name='Numéro'),
        ),
        migrations.AlterField(
            model_name='address',
            name='place_name',
            field=models.CharField(max_length=100, verbose_name='nom de voie'),
        ),
        migrations.AlterField(
            model_name='address',
            name='place_type',
            field=models.CharField(max_length=20, verbose_name='Type de voie'),
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.PositiveIntegerField(verbose_name='Code postal'),
        ),
        migrations.AlterField(
            model_name='address',
            name='remarks',
            field=models.CharField(max_length=200, verbose_name='Compléments'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Is_manager',
            field=models.BooleanField(verbose_name='Direction'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='diploma',
            field=models.CharField(max_length=100, verbose_name='Plus haut diplôme obtenu'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_contract',
            field=models.ImageField(upload_to='e_contracts', verbose_name='Scanner du contrat de travail'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_nr',
            field=models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name="Numéro d'employé"),
        ),
        migrations.AlterField(
            model_name='employee',
            name='occupation',
            field=models.CharField(max_length=100, verbose_name='Métier'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='IdScan',
            field=models.ImageField(upload_to='ids', verbose_name="Pièce d'identité"),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='phone',
            field=models.CharField(max_length=14, verbose_name="Téléphone d'urgence"),
        ),
    ]