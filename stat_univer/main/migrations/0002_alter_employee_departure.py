# Generated by Django 4.0.1 on 2022-01-27 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Departure',
            field=models.ForeignKey(blank=True, help_text='Выберите название кафедры', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.departure'),
        ),
    ]
