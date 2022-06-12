# Generated by Django 4.0.1 on 2022-06-12 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_monograph_departmentother_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250, verbose_name='Название публикации')),
                ('Output', models.CharField(max_length=250, verbose_name='Полное название конференции')),
                ('Year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('Pages', models.CharField(blank=True, max_length=50, null=True, verbose_name='Страницы')),
                ('DepartmentSame', models.CharField(blank=True, max_length=250, null=True, verbose_name='Авторы ГУУ с отчетной кафедры')),
                ('DepartmentOther', models.CharField(blank=True, max_length=250, null=True, verbose_name='Авторы с других кафедр ГУУ')),
                ('Url', models.URLField(blank=True, help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)', null=True, verbose_name='Ссылка на Ринц или сборник конференции')),
                ('Accepted', models.BooleanField(default=False, verbose_name='Принято')),
                ('Points', models.FloatField(blank=True, null=True, verbose_name='Количество баллов')),
                ('Comment', models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ')),
                ('Type', models.CharField(choices=[('', 'Выберите тип конференции'), ('M', 'Международная'), ('N', 'Национальная')], max_length=2, verbose_name='Тип конференции')),
                ('IdDeparture', models.ForeignKey(help_text='Выберите название кафедры.', on_delete=django.db.models.deletion.PROTECT, to='main.departure', verbose_name='Кафедра')),
                ('IdInstitute', models.ForeignKey(help_text='Выберите название института.', null=True, on_delete=django.db.models.deletion.PROTECT, to='main.institute', verbose_name='Институт')),
            ],
            options={
                'verbose_name': 'Тезис',
                'verbose_name_plural': 'Тезисы',
            },
        ),
        migrations.RemoveField(
            model_name='thesisworld',
            name='IdDeparture',
        ),
        migrations.RemoveField(
            model_name='thesisworld',
            name='IdInstitute',
        ),
        migrations.DeleteModel(
            name='ThesisNation',
        ),
        migrations.DeleteModel(
            name='ThesisWorld',
        ),
    ]