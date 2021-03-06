# Generated by Django 3.0.8 on 2020-08-18 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_access_admin', '0004_employee_familymember'),
        ('frontpage', '0009_auto_20200818_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=100, verbose_name='Prénom')),
                ('birth_date', models.DateField(verbose_name='Date de Naissance')),
                ('vaccine_next_due_date', models.DateField(verbose_name='Date de Prochaine Vaccination')),
                ('cc_facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Child_care_facility', verbose_name='Structure de Garde')),
            ],
            options={
                'verbose_name': 'Enfant',
                'verbose_name_plural': 'Enfants',
            },
        ),
        migrations.CreateModel(
            name='DailyFact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True, verbose_name='Horodatage')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='Commentaire général')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.Child', verbose_name='Enfant')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_access_admin.Employee', verbose_name='Employé')),
            ],
            options={
                'verbose_name': 'Donnée de Transmission',
                'verbose_name_plural': 'Données de Transmission',
            },
        ),
        migrations.CreateModel(
            name='EmployeeScheduledDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_arrival_time', models.TimeField(verbose_name="Heure d'Arrivée Planifiée")),
                ('scheduled_departure_time', models.TimeField(verbose_name='Heure de Départ Planifiée')),
                ('true_arrival_time_stamp', models.TimeField(auto_now_add=True, verbose_name="Heure d'Arrivée réelle")),
                ('true_departure_time_stamp', models.TimeField(auto_now_add=True, verbose_name='Heure de Départ réelle')),
                ('absence_motive', models.CharField(blank=True, max_length=100, verbose_name="Motif de l'absence")),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_access_admin.Employee', verbose_name='Employé')),
            ],
            options={
                'verbose_name': 'Jour de Planification Employé',
                'verbose_name_plural': 'Jours de Planification Employé',
            },
        ),
        migrations.CreateModel(
            name='ChildScheduledDay',
            fields=[
                ('employeescheduledday_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='day_to_day.EmployeeScheduledDay')),
            ],
            options={
                'verbose_name': 'Jour de Planification Enfants',
                'verbose_name_plural': 'Jours de Planification Enfants',
            },
            bases=('day_to_day.employeescheduledday',),
        ),
        migrations.CreateModel(
            name='Sleep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length_minutes', models.PositiveSmallIntegerField(verbose_name='Durée')),
                ('daily_fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.DailyFact', verbose_name='Transmission')),
            ],
            options={
                'verbose_name': 'Sieste',
                'verbose_name_plural': 'Siestes',
            },
        ),
        migrations.CreateModel(
            name='OpenDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('opening_H', models.TimeField(verbose_name="Heure d'Ouverture")),
                ('closing_H', models.TimeField(verbose_name='Heure de Fermeture')),
                ('planified_Structure', models.ManyToManyField(to='frontpage.Child_care_facility', verbose_name="Jour d'Ouverture Structure")),
                ('planified_employee', models.ManyToManyField(blank=True, through='day_to_day.EmployeeScheduledDay', to='auth_access_admin.Employee', verbose_name='Employé planifié')),
            ],
            options={
                'verbose_name': "Jour et heure d'ouverture",
                'verbose_name_plural': "Jours et heures d'ouverture",
            },
        ),
        migrations.CreateModel(
            name='MedicalEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('body_temp_deg_C', models.DecimalField(blank=True, decimal_places=2, max_digits=3, verbose_name='Température')),
                ('given_paracetamol_qtty_mg', models.PositiveSmallIntegerField(blank=True, verbose_name='Paracétamol donné / mg')),
                ('daily_fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.DailyFact', verbose_name='Transmission')),
            ],
            options={
                'verbose_name': 'Evènement Médical',
                'verbose_name_plural': 'Evènements Médicaux',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starter_qtty_gr', models.PositiveSmallIntegerField(blank=True, verbose_name='Entrée')),
                ('main_course_qtty_gr', models.PositiveSmallIntegerField(blank=True, verbose_name='Plat de résistance')),
                ('desert_qtty_gr', models.PositiveSmallIntegerField(blank=True, verbose_name='Déssert')),
                ('daily_fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.DailyFact', verbose_name='Transmission')),
            ],
            options={
                'verbose_name': 'Repas',
                'verbose_name_plural': 'Repas',
            },
        ),
        migrations.CreateModel(
            name='FeedingBottle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prepared_qtty_ml', models.PositiveSmallIntegerField(verbose_name='Quantité Préparée ml')),
                ('drank_qtty_ml', models.PositiveSmallIntegerField(verbose_name='Quantité Bue ml')),
                ('daily_fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.DailyFact', verbose_name='Transmission')),
            ],
            options={
                'verbose_name': 'Biberon',
                'verbose_name_plural': 'Biberons',
            },
        ),
        migrations.CreateModel(
            name='Family_link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_type', models.CharField(max_length=50, verbose_name='Lien Familial')),
                ('retrieval_auth', models.BooleanField(default=False, verbose_name='Autorisation de Prise en Charge')),
                ('emergency_contact_person', models.BooleanField(default=False, verbose_name="Contact en cas d'urgence")),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.Child', verbose_name='Enfant')),
                ('relative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_access_admin.FamilyMember', verbose_name='Membre Familial')),
            ],
            options={
                'verbose_name': 'Lien de parenté',
                'verbose_name_plural': 'Liens de parenté',
            },
        ),
        migrations.AddField(
            model_name='employeescheduledday',
            name='open_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.OpenDay', verbose_name="Jour d'ouverture"),
        ),
        migrations.AddField(
            model_name='child',
            name='relative',
            field=models.ManyToManyField(through='day_to_day.Family_link', to='auth_access_admin.FamilyMember'),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('MF', 'Motricité Fine'), ('M', 'Motricité'), ('SP', 'Sport')], max_length=2, verbose_name="Type d'Activité")),
                ('period', models.CharField(choices=[('AM', 'Matin'), ('PM', 'Après-Midi')], max_length=2, verbose_name='Période')),
                ('daily_fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.DailyFact', verbose_name='Transmission')),
            ],
            options={
                'verbose_name': 'Activité',
                'verbose_name_plural': 'Activités',
            },
        ),
        migrations.AddField(
            model_name='openday',
            name='planified_child',
            field=models.ManyToManyField(blank=True, through='day_to_day.ChildScheduledDay', to='day_to_day.Child', verbose_name='Enfant planifié'),
        ),
        migrations.AddField(
            model_name='childscheduledday',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='day_to_day.Child', verbose_name='Enfant'),
        ),
    ]
