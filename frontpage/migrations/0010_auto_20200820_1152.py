# Generated by Django 3.0.8 on 2020-08-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0009_auto_20200818_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
    ]
