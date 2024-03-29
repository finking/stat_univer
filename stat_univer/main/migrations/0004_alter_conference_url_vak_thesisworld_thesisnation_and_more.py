# Generated by Django 4.0.2 on 2022-05-26 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_conference_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='Url',
            field=models.URLField(blank=True, help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)', verbose_name='Ссылка на конференцию:'),
        ),
        migrations.CreateModel(
            name='VAK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250, verbose_name='Название публикации')),
                ('Year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('Pages', models.CharField(blank=True, max_length=50, null=True, verbose_name='Страницы')),
                ('DepartmentSame', models.CharField(max_length=250, verbose_name='Авторы ГУУ с отчетной кафедры')),
                ('DepartmentOther', models.CharField(max_length=250, verbose_name='Авторы с других кафедр ГУУ')),
                ('Accepted', models.BooleanField(default=False, verbose_name='Принято')),
                ('Points', models.FloatField(blank=True, null=True, verbose_name='Количество баллов')),
                ('Comment', models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ')),
                ('Type', models.CharField(max_length=250, verbose_name='Публикация ВАК')),
                ('Tom', models.CharField(blank=True, max_length=250, null=True, verbose_name='Том')),
                ('Output', models.CharField(max_length=250, verbose_name='Название журнала')),
                ('Url', models.URLField(blank=True, help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)', null=True, verbose_name='Ссылка на Ринц или публикацию в журнале')),
                ('IdDeparture', models.ForeignKey(help_text='Выберите название кафедры.', on_delete=django.db.models.deletion.PROTECT, to='main.departure', verbose_name='Кафедра')),
                ('IdInstitute', models.ForeignKey(help_text='Выберите название института.', null=True, on_delete=django.db.models.deletion.PROTECT, to='main.institute', verbose_name='Институт')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThesisWorld',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250, verbose_name='Название публикации')),
                ('Output', models.CharField(max_length=250, verbose_name='Полное название конференции')),
                ('Year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('Pages', models.CharField(blank=True, max_length=50, null=True, verbose_name='Страницы')),
                ('DepartmentSame', models.CharField(max_length=250, verbose_name='Авторы ГУУ с отчетной кафедры')),
                ('DepartmentOther', models.CharField(max_length=250, verbose_name='Авторы с других кафедр ГУУ')),
                ('Url', models.URLField(blank=True, help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)', null=True, verbose_name='Ссылка на Ринц или сборник конференции')),
                ('Accepted', models.BooleanField(default=False, verbose_name='Принято')),
                ('Points', models.FloatField(blank=True, null=True, verbose_name='Количество баллов')),
                ('Comment', models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ')),
                ('Type', models.CharField(max_length=250, verbose_name='Тезисы на международных конференциях')),
                ('IdDeparture', models.ForeignKey(help_text='Выберите название кафедры.', on_delete=django.db.models.deletion.PROTECT, to='main.departure', verbose_name='Кафедра')),
                ('IdInstitute', models.ForeignKey(help_text='Выберите название института.', null=True, on_delete=django.db.models.deletion.PROTECT, to='main.institute', verbose_name='Институт')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThesisNation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250, verbose_name='Название публикации')),
                ('Output', models.CharField(max_length=250, verbose_name='Полное название конференции')),
                ('Year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('Pages', models.CharField(blank=True, max_length=50, null=True, verbose_name='Страницы')),
                ('DepartmentSame', models.CharField(max_length=250, verbose_name='Авторы ГУУ с отчетной кафедры')),
                ('DepartmentOther', models.CharField(max_length=250, verbose_name='Авторы с других кафедр ГУУ')),
                ('Url', models.URLField(blank=True, help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)', null=True, verbose_name='Ссылка на Ринц или сборник конференции')),
                ('Accepted', models.BooleanField(default=False, verbose_name='Принято')),
                ('Points', models.FloatField(blank=True, null=True, verbose_name='Количество баллов')),
                ('Comment', models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ')),
                ('Type', models.CharField(max_length=250, verbose_name='Тезисы на национальных конференциях')),
                ('IdDeparture', models.ForeignKey(help_text='Выберите название кафедры.', on_delete=django.db.models.deletion.PROTECT, to='main.departure', verbose_name='Кафедра')),
                ('IdInstitute', models.ForeignKey(help_text='Выберите название института.', null=True, on_delete=django.db.models.deletion.PROTECT, to='main.institute', verbose_name='Институт')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Monograph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250, verbose_name='Название публикации')),
                ('Year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('Pages', models.CharField(blank=True, max_length=50, null=True, verbose_name='Страницы')),
                ('DepartmentSame', models.CharField(max_length=250, verbose_name='Авторы ГУУ с отчетной кафедры')),
                ('DepartmentOther', models.CharField(max_length=250, verbose_name='Авторы с других кафедр ГУУ')),
                ('Accepted', models.BooleanField(default=False, verbose_name='Принято')),
                ('Points', models.FloatField(blank=True, null=True, verbose_name='Количество баллов')),
                ('Comment', models.TextField(blank=True, null=True, verbose_name='Комментарий УКНИ')),
                ('Output', models.CharField(blank=True, max_length=100, null=True, verbose_name='ISBN')),
                ('Url', models.URLField(blank=True, help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)', null=True, verbose_name='Ссылка на Ринц или на файл pdf, загруженный на стороннем ресурсе')),
                ('IdDeparture', models.ForeignKey(help_text='Выберите название кафедры.', on_delete=django.db.models.deletion.PROTECT, to='main.departure', verbose_name='Кафедра')),
                ('IdInstitute', models.ForeignKey(help_text='Выберите название института.', null=True, on_delete=django.db.models.deletion.PROTECT, to='main.institute', verbose_name='Институт')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
