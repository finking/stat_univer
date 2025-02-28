from django.core.mail import send_mail

# Adding setting
# https://qna.habr.com/q/701205
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
STAFF_MAIL_FROM = env('STAFF_MAIL_FROM')
STAFF_MAIL_TO = env('STAFF_MAIL_TO')
ERROR_LOG_FILENAME = 'log_error.log'


# Отправка email-уведомления
def send_mail_staff(nameRecord, url, department, username, new=True):
    """
    Функция отправки сообщения сотрудникам, которые проверяют внесение данных
    
    :param nameRecord: Название записи (публикации, НИР или РИД)
    :param url: Ссылка на запись
    :param department: Название кафедры
    :param username: Имя пользователя, который довабляет публикацию
    :param new: True - Новая публикация, иначе редактирование уже имеющейся
    """
    
    subject = f'{department} добавила данные.' if new else f'{department} внесла изменения.'
    
    message = \
        f'Пользователь {username} добавил запись для: {department}. \r\n' f'Название: {nameRecord}. \r\nСсылка: {url}' \
            if new else f'{department} внесла изменения в {nameRecord}: {url}'
    
    send_mail(subject,
              message,
              STAFF_MAIL_FROM,
              STAFF_MAIL_TO.split(','),
              fail_silently=False,
              )


STATUS = (
    ('', 'Выберите статус'),
    ('М', 'Международная'),
    ('Р', 'Российская'),
    ('Ре', 'Региональная')
)

TYPECONFERENCE = (
    ('', 'Выберите тип конференции'),
    ('M', 'Международная'),
    ('N', 'Национальная'),
)

BINAR = (
    ('', 'Выберите да/нет'),
    ('Y', 'Да'),
    ('N', 'Нет'),
)

MONTH = (
    ('', 'Выберите месяц'),
    ('Ja', 'Январь'),
    ('Fe', 'Февраль'),
    ('Mar', 'Март'),
    ('Ap', 'Апрель'),
    ('May', 'Май'),
    ('Jun', 'Июнь'),
    ('Jul', 'Июль'),
    ('Au', 'Август'),
    ('Se', 'Сентябрь'),
    ('Oc', 'Октябрь'),
    ('No', 'Ноябрь'),
    ('De', 'Декабрь'),
)

POSIZION = (
    ('', 'Выберите должность'),
    ('МНС', 'младший научный сотрудник'),
    ('НС', 'научный сотрудник'),
    ('СНС', 'старший научный сотрудник'),
    ('ВНС', 'ведущий научный сотрудник'),
    ('ГНС', 'главный научный сотрудник'),
    ('АП', 'ассистент преподавателя'),
    ('ПР', 'преподаватель'),
    ('СПР', 'старший преподаватель'),
    ('ДОЦ', 'доцент'),
    ('ПРОФ', 'профессор'),
    ('НР', 'научный работник'),
    ('ИТР', 'инженерно-технический работник'),
    ('ДР', 'другое')
)

DEGREE = (
    ('', 'Выберите степень'),
    ('ДОКТ', 'доктор'),
    ('КАНД', 'кандидат'),
    ('БС', 'без степени')
)

TYPEWORK = (
    ('', 'Выберите тип'),
    ('О', 'основной'),
    ('В', 'внешний'),
)

COUNTRY = (
    ('', 'Выберите страну'),
    ('RU', 'Россия'),
    ('AB', 'Абхазия'),
    ('AU', 'Австралия'),
    ('AT', 'Австрия'),
    ('AZ', 'Азербайджан'),
    ('AL', 'Албания'),
    ('DZ', 'Алжир'),
    ('AI', 'Ангилья'),
    ('AO', 'Ангола'),
    ('AD', 'Андорра'),
    ('AR', 'Аргентина'),
    ('AM', 'Армения'),
    ('AW', 'Аруба'),
    ('AF', 'Афганистан'),
    ('BS', 'Багамы'),
    ('BD', 'Бангладеш'),
    ('BB', 'Барбадос'),
    ('BH', 'Бахрейн'),
    ('BY', 'Беларусь'),
    ('BZ', 'Белиз'),
    ('BE', 'Бельгия'),
    ('BJ', 'Бенин'),
    ('BM', 'Бермуды'),
    ('BG', 'Болгария'),
    ('BO', 'Боливия'),
    ('BA', 'Босния и Герцеговина'),
    ('BW', 'Ботсвана'),
    ('BR', 'Бразилия'),
    ('BN', 'Бруней-Даруссалам'),
    ('BF', 'Буркина-Фасо'),
    ('BI', 'Бурунди'),
    ('BT', 'Бутан'),
    ('VU', 'Вануату'),
    ('GB', 'Великобритания'),
    ('HU', 'Венгрия'),
    ('VE', 'Венесуэла'),
    ('VN', 'Вьетнам'),
    ('GA', 'Габон'),
    ('HT', 'Гаити'),
    ('GY', 'Гайана'),
    ('GM', 'Гамбия'),
    ('GH', 'Гана'),
    ('GP', 'Гваделупа'),
    ('GT', 'Гватемала'),
    ('GN', 'Гвинея'),
    ('GW', 'Гвинея-Бисау'),
    ('DE', 'Германия'),
    ('GI', 'Гибралтар'),
    ('HN', 'Гондурас'),
    ('HK', 'Гонконг'),
    ('GD', 'Гренада'),
    ('GL', 'Гренландия'),
    ('GR', 'Греция'),
    ('GE', 'Грузия'),
    ('GU', 'Гуам'),
    ('DK', 'Дания'),
    ('JE', 'Джерси'),
    ('DJ', 'Джибути'),
    ('DM', 'Доминика'),
    ('DO', 'ДоминиканскаяРеспублика'),
    ('EG', 'Египет'),
    ('ZM', 'Замбия'),
    ('ZW', 'Зимбабве'),
    ('IL', 'Израиль'),
    ('IN', 'Индия'),
    ('ID', 'Индонезия'),
    ('JO', 'Иордания'),
    ('IQ', 'Ирак'),
    ('IR', 'Иран'),
    ('IE', 'Ирландия'),
    ('IS', 'Исландия'),
    ('ES', 'Испания'),
    ('IT', 'Италия'),
    ('YE', 'Йемен'),
    ('CV', 'Кабо-Верде'),
    ('KZ', 'Казахстан'),
    ('KH', 'Камбоджа'),
    ('CM', 'Камерун'),
    ('CA', 'Канада'),
    ('QA', 'Катар'),
    ('KE', 'Кения'),
    ('CY', 'Кипр'),
    ('KG', 'Киргизия'),
    ('CN', 'Китай'),
    ('CO', 'Колумбия'),
    ('KM', 'Коморы'),
    ('CG', 'Конго'),
    ('CD', 'Конго'),
    ('KP', 'КНДР'),
    ('KR', 'Республика Корея'),
    ('CR', 'Коста-Рика'),
    ('CU', 'Куба'),
    ('KW', 'Кувейт'),
    ('CW', 'Кюрасао'),
    ('LA', 'Лаос'),
    ('LV', 'Латвия'),
    ('LS', 'Лесото'),
    ('LB', 'Ливан'),
    ('LY', 'Ливийская Арабская Джамахирия'),
    ('LR', 'Либерия'),
    ('LI', 'Лихтенштейн'),
    ('LT', 'Литва'),
    ('LU', 'Люксембург'),
    ('MU', 'Маврикий'),
    ('MR', 'Мавритания'),
    ('MG', 'Мадагаскар'),
    ('YT', 'Майотта'),
    ('MO', 'Макао'),
    ('MW', 'Малави'),
    ('MY', 'Малайзия'),
    ('ML', 'Мали'),
    ('MV', 'Мальдивы'),
    ('MT', 'Мальта'),
    ('MA', 'Марокко'),
    ('MQ', 'Мартиника'),
    ('MX', 'Мексика'),
    ('MZ', 'Мозамбик'),
    ('MD', 'Молдова'),
    ('MC', 'Монако'),
    ('MN', 'Монголия'),
    ('MS', 'Монтсеррат'),
    ('MM', 'Мьянма'),
    ('NA', 'Намибия'),
    ('NR', 'Науру'),
    ('NP', 'Непал'),
    ('NE', 'Нигер'),
    ('NG', 'Нигерия'),
    ('NL', 'Нидерланды'),
    ('NI', 'Никарагуа'),
    ('NZ', 'Новая Зеландия'),
    ('NC', 'Новая Каледония'),
    ('NO', 'Норвегия'),
    ('AE', 'ОАЭ'),
    ('OM', 'Оман'),
    ('PK', 'Пакистан'),
    ('PA', 'Панама'),
    ('PG', 'Папуа-Новая Гвинея'),
    ('PY', 'Парагвай'),
    ('PE', 'Перу'),
    ('PL', 'Польша'),
    ('PT', 'Португалия'),
    ('PR', 'Пуэрто-Рико'),
    ('MK', 'Республика Македония'),
    ('RW', 'Руанда'),
    ('RO', 'Румыния'),
    ('WS', 'Самоа'),
    ('SM', 'Сан-Марино'),
    ('SA', 'СаудовскаяАравия'),
    ('SN', 'Сенегал'),
    ('RS', 'Сербия'),
    ('SC', 'Сейшелы'),
    ('SG', 'Сингапур'),
    ('SY', 'Сирийская Арабская Республика'),
    ('SK', 'Словакия'),
    ('SI', 'Словения'),
    ('US', 'Соединенные Штаты'),
    ('SO', 'Сомали'),
    ('SD', 'Судан'),
    ('SR', 'Суринам'),
    ('SL', 'Сьерра-Леоне'),
    ('TJ', 'Таджикистан'),
    ('TH', 'Таиланд'),
    ('TW', 'Тайвань (Китай)'),
    ('TZ', 'Танзания'),
    ('TL', 'Тимор-Лесте'),
    ('TG', 'Того'),
    ('TK', 'Токелау'),
    ('TO', 'Тонга'),
    ('TT', 'Тринидади Тобаго'),
    ('TV', 'Тувалу'),
    ('TN', 'Тунис'),
    ('TM', 'Туркмения'),
    ('TR', 'Турция'),
    ('UG', 'Уганда'),
    ('UZ', 'Узбекистан'),
    ('UA', 'Украина'),
    ('UY', 'Уругвай'),
    ('FO', 'Фарерские острова'),
    ('FJ', 'Фиджи'),
    ('PH', 'Филиппины'),
    ('FI', 'Финляндия'),
    ('FR', 'Франция'),
    ('HR', 'Хорватия'),
    ('CF', 'Центрально-Африканская Республика'),
    ('TD', 'Чад'),
    ('ME', 'Черногория'),
    ('CZ', 'Чехия'),
    ('CL', 'Чили'),
    ('CH', 'Швейцария'),
    ('SE', 'Швеция'),
    ('LK', 'Шри-Ланка'),
    ('EC', 'Эквадор'),
    ('GQ', 'Экваториальная Гвинея'),
    ('EE', 'Эстония'),
    ('ET', 'Эфиопия'),
    ('ZA', 'Южная Африка'),
    ('OS', 'Южная Осетия'),
    ('SS', 'Южный Судан'),
    ('JM', 'Ямайка'),
    ('JP', 'Япония')
)

PARAMETERNAME = (
    ('', 'Выберите показатель'),
    ('ВАК', 'Количество публикаций в журналах ВАК'),
    ('ТЕЗИСЫ_М', 'Количество тезисов в международных конференциях'),
    ('ТЕЗИСЫ_Н', 'Количество тезисов в национальных конференциях'),
    ('МОНОГРАФИЯ', 'Количество монографий'),
    ('ДОХОД', 'Общий доход, руб.'),
    ('РИД', 'РИД'),
)
