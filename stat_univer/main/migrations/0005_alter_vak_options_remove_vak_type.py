# Generated by Django 4.0.2 on 2022-05-26 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_conference_url_vak_thesisworld_thesisnation_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vak',
            options={'verbose_name': 'Публикация ВАК', 'verbose_name_plural': 'Публикации ВАК'},
        ),
        migrations.RemoveField(
            model_name='vak',
            name='Type',
        ),
    ]