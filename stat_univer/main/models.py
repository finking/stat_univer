from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse

from .utils import *


class Institute(models.Model):
    Name = models.CharField('Название', max_length=70,
                            error_messages={'required': 'Please enter your initial_feature'})
    ShortName = models.CharField('Аббревиатура', max_length=10)
    Director = models.ForeignKey(
        'Employee',
        related_name='Director',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default='No',
        verbose_name='Директор'
    )
    DeputeScience = models.ForeignKey(
        'Employee',
        related_name='Depute',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default='No',
        verbose_name='Зам.директора по науке'
    )

    class Meta:
        verbose_name = "Институт"
        verbose_name_plural = "Институты"

    def __str__(self):
        return self.Name


# # Проверка наличие 4 цифры в Годе рождения и в СНИЛС
# # https://docs.djangoproject.com/en/dev/ref/validators/
# def validate_four(value):
#     if len(value) != 4:
#         raise ValidationError(
#             gettext_lazy('Указано %(value) цифры. Должно быть 4'),
#             params={'value': value}
#         )  # TODO перенести в отдельный файл по примеру: https://stackoverflow.com/questions/5437985/django-alphanumeric-charfield
# # Update 27.01. При миграции получил ошибку. Подчеркивает import main.models Т.е. не видит этот путь


class Employee(models.Model):
    Name = models.CharField('Имя',
                            max_length=20,
                            help_text='Введите имя.')
    MiddleName = models.CharField('Отчество',
                                  max_length=20,
                                  blank=True,
                                  help_text='Введите отчество (при наличии).')
    Surname = models.CharField('Фамилия',
                               max_length=30,
                               help_text='Введите фамилию.')
    PrevSurname = models.CharField('Предыдущая Фамилия',
                                   max_length=30,
                                   blank=True,
                                   default='No',
                                   help_text='Если меняли фамилию, то введите предыдущую.')
    Position = models.CharField('Должность',
                                choices=POSIZION,
                                max_length=20,
                                help_text='Выберите должность.')
    Degree = models.CharField('Ученая степень',
                              choices=DEGREE,
                              max_length=20,
                              help_text='Выберете ученую степень.',
                              blank=True,
                              default='No'
                              )
    TypeWork = models.CharField('Тип трудовых отношений',
                                choices=TYPEWORK,
                                max_length=20,
                                help_text='Выберете тип трудовых отношений.')
    Year = models.CharField('Год рождения',
                            help_text='Введите год рождения',
                            max_length=4,
                            blank=True,
                            default='1900'
                            # validators=[validate_four]
                            )
    Identifier = models.CharField('СНИЛС',
                                  help_text='Введите 4 последние цифры СНИЛС.',
                                  max_length=4,
                                  blank=True,
                                  default='0000'
                                  # validators=[validate_four]
                                  )
    Email = models.EmailField('Email', help_text='Введите email')
    Departure = models.ForeignKey(
        'Departure',
        verbose_name='Кафедра',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Выберите название кафедры.',
        blank=True
    )

    class Meta:
        verbose_name = "Сотрудника"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f'{self.Surname} {self.Name} {self.MiddleName}'


class Departure(models.Model):
    Name = models.CharField('Название', max_length=80)
    Institute = models.ForeignKey(
        'Institute',
        verbose_name='Институт',
        on_delete=models.SET_NULL, null=True, help_text='Выберите название института.'
    )

    class Meta:
        verbose_name = "Кафедру"
        verbose_name_plural = "Кафедры"

    def __str__(self):
        return self.Name
    
    # Получение фактического количества статей ВАК
    def get_fact_vak(self, year):
        return self.vak_set.filter(Year=year, Accepted=True).aggregate(sum=Sum('Points'))['sum']
    
    # Получение фактического количества тезисов
    def get_fact_thesis(self, year, type='M'):
        return self.thesis_set.filter(Year=year, Accepted=True, Type=type).aggregate(sum=Sum('Points'))['sum']
    
    # Получение фактического количества монографий
    def get_fact_monograph(self, year):
        return self.monograph_set.filter(Year=year, Accepted=True).aggregate(sum=Sum('Points'))['sum']
    
    # Получение фактического количества РИД
    def get_fact_rid(self, year):
        return self.rid_set.filter(Year=year, Accepted=True).aggregate(sum=Sum('Points'))['sum']
    
    # Получение фактического Дохода
    def get_fact_income(self, year):
        return self.income_set.filter(Year=year, Accepted=True).aggregate(sum=Sum('Points'))['sum']



class Conference(models.Model):
    Name = models.CharField('Название конференции:', max_length=255)

    Country = models.CharField('Страна проведения:',
                               choices=COUNTRY,
                               max_length=2)
    City = models.CharField('Город проведения:', max_length=30)

    Status = models.CharField('Статус:',
                              help_text='Выберите из списка.',
                              choices=STATUS,
                              max_length=2)

    Month = models.CharField('Месяц проведения:',
                             choices=MONTH,
                             max_length=3,
                             default='')

    Organizer = models.BooleanField('Организатор ГУУ', default=False,
                                    help_text='Поставьте галочку, если ГУУ является '
                                                                   'организатором конференции.')

    Student = models.BooleanField('Студенческая', default=False,
                                  help_text='Поставьте галочку, если конференция является студенческой.')

    Total = models.IntegerField('Общее число участников:',
                                help_text='Введите примерное количество участников.')
    Delegate = models.IntegerField('В том числе от ГУУ:',
                                   help_text='Введите количество представителей ГУУ, участвующих в конференции.')
    # Общее количество студентов (для конференций, организованных вузом)
    Total_student = models.IntegerField('Общее число студентов:',
                                help_text='Введите количество студентов, принявших участие.',
                                blank=True,
                                null=True)
    # Количество собственных студентов, принявших участие в конференции
    Delegate_student = models.IntegerField('В том числе студентов из ГУУ:',
                                   help_text='Введите количество студентов ГУУ, участвующих в конференции.',
                                   blank=True,
                                   null=True
                                   )
    Url = models.URLField('Ссылка на конференцию:',
                          help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)',
                          blank=True,
                          null=False)
    Email = models.EmailField('Email:',
                              help_text='Укажите свой email. По данному email можно видеть все внесенные Вами конференции.',
                              blank=True,
                              null=True)
    Invite = models.TextField('Список организаций, в которые отправлены приглашения:',
                              help_text='Введите организации (через запятую).',
                              blank=True, null=True)

    TimeCreate = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = "Конференцию"
        verbose_name_plural = "Конференции"

    def __str__(self):
        return self.Name
    
    # Функция преобразования True/False для записи в файл
    def get_student_display(self):
        return "да" if self.Student else "нет"

    # Функция преобразования True/False для записи в файл
    def get_organizer_display(self):
        return "да" if self.Organizer else "нет"

    # Функция преобразования даты для записи в файл
    def get_timeCreate(self):
        return self.TimeCreate.strftime("%d-%m-%Y %H:%M:%S")


class FAQ(models.Model):
    Question = models.CharField('Вопрос', max_length=250)

    Answer = models.TextField('Ответ')

    Link = models.URLField('Ссылка на видео (при наличии)',
                          help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)',
                          blank=True,
                          null=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.Question


class BaseModel(models.Model):
    class Meta:
        abstract = True

    Year = models.IntegerField('Год')
    DepartmentSame = models.CharField('Авторы ГУУ с отчетной кафедры', max_length=250)
    DepartmentOther = models.CharField('Авторы с других кафедр ГУУ',
                                       max_length=250,
                                       blank=True,
                                       null=True)
    Accepted = models.BooleanField('Принято: ', default=False)
    Points = models.FloatField('Количество баллов: ',
                               default=0,
                               blank=True)
    Comment = models.TextField('Комментарий отдела статистики: ',
                               blank=True,
                               null=True)
    Departure = models.ForeignKey(
        'Departure',
        verbose_name='Кафедра',
        on_delete=models.PROTECT,
        help_text='Выберите название кафедры.'
    )

    Author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    DateCreated = models.DateTimeField(auto_now_add=True, verbose_name='Дата внесения')
    DateUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # Используем lowercase название модели как часть URL
        model_name = self._meta.model_name
        return reverse(f'{model_name}_update', kwargs={'pk': self.pk})
    
    # Функция преобразования True/False для записи в файл
    def get_accepted_display(self):
        return "да" if self.Accepted else "нет"

    # Функция преобразования даты для записи в файл
    def get_date_created(self):
        return self.DateCreated.strftime("%d-%m-%Y %H:%M:%S")
    
    def get_date_updated(self):
        return self.DateUpdated.strftime("%d-%m-%Y %H:%M:%S")
    
class Publication(BaseModel):
    class Meta:
        abstract = True
        
    Name = models.CharField('Название публикации', max_length=250)
    Output = models.CharField('Полное название конференции', max_length=250)
    Pages = models.CharField('Страницы', max_length=50,
                                blank=True,
                                null=True)

    Url = models.URLField('Ссылка на Ринц или сборник конференции', max_length=500,
                          help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)',
                          blank=True,
                          null=True)


class VAK(Publication):
    class Meta:
        verbose_name = "Публикация ВАК"
        verbose_name_plural = "Публикации ВАК"
        
    def __str__(self):
        return self.Name
    
    Tom = models.CharField('Том',
                           max_length=250,
                           blank=True,
                           null=True)
    Output = models.CharField('Название журнала', max_length=250)
    Url = models.URLField('Ссылка на Ринц')


class Thesis(Publication):
    class Meta:
        verbose_name = "Тезис"
        verbose_name_plural = "Тезисы"

    def __str__(self):
        return self.Name

    Type = models.CharField('Тип конференции',
                              choices=TYPECONFERENCE,
                              max_length=2)
    
    
class Monograph(Publication):
    class Meta:
        verbose_name = "Монография"
        verbose_name_plural = "Монографии"
    
    def __str__(self):
        return self.Name
    
    Name = models.CharField('Название монографии', max_length=250)
    
    Output = models.CharField('ISBN',
                              max_length=100)
    
    Url = models.URLField('Ссылка на Ринц или на файл pdf, загруженный на стороннем ресурсе',
                          help_text='Ссылка должна начинаться с http:// или https:// (например: https://yandex.ru/)',
                          blank=True,
                          null=True)


class Income(BaseModel):
    class Meta:
        verbose_name = "Доход"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Name
    
    Name = models.CharField('Наименование НИР (работы, услуги)', max_length=500)
    Value = models.FloatField('Сумма НИР', default=0,  help_text='Укажите сумму договора')


class RID(BaseModel):
    class Meta:
        verbose_name = "РИД"
        verbose_name_plural = "РИДы"

    def __str__(self):
        return self.Name
    
    Name = models.CharField('Наименование РИД', max_length=500)
    Doc = models.FileField(verbose_name='Свидетельство', upload_to='docs', default=None,
                           max_length=300)
    

class Plan(models.Model):
    class Meta:
        verbose_name = "Плановые показатели"
        verbose_name_plural = verbose_name

    Departure = models.ForeignKey('Departure', verbose_name='Кафедра', on_delete=models.CASCADE, default='-')
    Name = models.CharField('Показатель', choices=PARAMETERNAME, max_length=10)
    Year = models.IntegerField('Год')
    Value = models.FloatField('Значение (в шт) или Сумма (в руб.)', default=0)
    DateCreated = models.DateTimeField(auto_now_add=True, verbose_name='Дата внесения')
    DateUpdated = models.DateTimeField(auto_now=True)
