# Generated by Django 3.0.8 on 2020-08-20 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_access_admin', '0004_employee_familymember'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Salarié', 'verbose_name_plural': 'Salariés'},
        ),
        migrations.AlterModelOptions(
            name='familymember',
            options={'verbose_name': 'Membre Familial', 'verbose_name_plural': 'Membres de la Famille'},
        ),
    ]