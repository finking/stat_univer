# Generated by Django 4.0.2 on 2022-08-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_monograph_admitted_thesis_admitted_vak_admitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monograph',
            name='Admitted',
        ),
        migrations.RemoveField(
            model_name='thesis',
            name='Admitted',
        ),
        migrations.RemoveField(
            model_name='vak',
            name='Admitted',
        ),
        migrations.AlterField(
            model_name='monograph',
            name='Accepted',
            field=models.BooleanField(default=False, verbose_name='Принято: '),
        ),
        migrations.AlterField(
            model_name='monograph',
            name='Comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ: '),
        ),
        migrations.AlterField(
            model_name='monograph',
            name='Points',
            field=models.FloatField(default=0, verbose_name='Количество баллов: '),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='Accepted',
            field=models.BooleanField(default=False, verbose_name='Принято: '),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='Comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ: '),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='Points',
            field=models.FloatField(default=0, verbose_name='Количество баллов: '),
        ),
        migrations.AlterField(
            model_name='vak',
            name='Accepted',
            field=models.BooleanField(default=False, verbose_name='Принято: '),
        ),
        migrations.AlterField(
            model_name='vak',
            name='Comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ: '),
        ),
        migrations.AlterField(
            model_name='vak',
            name='Points',
            field=models.FloatField(default=0, verbose_name='Количество баллов: '),
        ),
    ]
