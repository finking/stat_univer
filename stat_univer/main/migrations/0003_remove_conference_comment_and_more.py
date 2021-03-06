# Generated by Django 4.0.2 on 2022-03-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_faq_alter_employee_options_alter_conference_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='Comment',
        ),
        migrations.AddField(
            model_name='conference',
            name='Delegate_student',
            field=models.IntegerField(blank=True, help_text='Введите количество студентов ГУУ, участвующих в конференции.', null=True, verbose_name='В том числе студентов из ГУУ:'),
        ),
        migrations.AddField(
            model_name='conference',
            name='Invite',
            field=models.TextField(blank=True, help_text='Введите организации (через запятую).', null=True, verbose_name='Список организаций, в которые отправлены приглашения:'),
        ),
        migrations.AddField(
            model_name='conference',
            name='Total_student',
            field=models.IntegerField(blank=True, help_text='Введите количество студентов, принявших участие.', null=True, verbose_name='Общее число студентов:'),
        ),
    ]
