# Generated by Django 3.0.8 on 2020-08-18 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0008_auto_20200812_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='child_care_facility',
            options={'verbose_name': 'Structure de Garde', 'verbose_name_plural': 'Structures de Garde'},
        ),
        migrations.AlterModelOptions(
            name='new',
            options={'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
        migrations.AlterField(
            model_name='new',
            name='cc_facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Child_care_facility', verbose_name='Structure de Garde'),
        ),
    ]
