# Generated by Django 3.0.8 on 2020-08-20 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day_to_day', '0004_auto_20200820_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(max_length=200, verbose_name='Contenu'),
        ),
    ]
