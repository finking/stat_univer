# Generated by Django 4.0.1 on 2022-02-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_conference_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='Organizer',
            field=models.BinaryField(blank=True, default=True, null=True, verbose_name='Организатор ГУУ:'),
        ),
    ]
