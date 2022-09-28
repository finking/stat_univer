from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Institute, Conference, Employee, FAQ, VAK, Thesis, Departure
from .forms import ConferenceForm, HistoryForm, VAKForm, ThesisForm
from django.http import HttpResponse
from datetime import datetime
from xlsxwriter.workbook import Workbook
import io
import logging
from .utils import dict_from_tuple, binary, MONTH, STATUS, COUNTRY, DepartureTemplate
from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Загрузка главной страницы. Шаблон: index.html')
    return render(request, 'main/index.html')


def vvod(request):
    logger.info('Загрузка страницы ввода. Шаблон: vvod.html')
    return render(request, 'main/vvod.html')


def success(request):
    logger.info('Загрузка успешной отправки формы. Шаблон: success.html')
    return render(request, 'main/success.html')


def institute(request):
    logger.info('Загрузка страницы с Институтами. Шаблон: institute.html')
    dictInstitute = {}
    institutes = Institute.objects.order_by('-id')
    if institutes:
        for i in institutes:
            NameInstitute = i.Name
            Director = Employee.objects.filter(Name=i.IdDirector)
            dictInstitute.setdefault(NameInstitute, Director)
        logger.debug(dictInstitute)
    error = ''
    
    return render(request, 'main/institute.html', {'title': 'Институты ГУУ',
                                                   'institutes': institutes,
                                                   # 'form': form,
                                                   'error': error})


def department(request):
    logger.info('Загрузка страницы с Кафедрами. Шаблон: department.html')
    return render(request, 'main/department.html')


def lecturer(request):
    logger.info('Загрузка страницы с Преподавателями. Шаблон: lecturer.html')
    return render(request, 'main/lecturer.html')


def conference(request):
    logger.info('Загрузка страницы с формой по Конференциям. Шаблон: conference.html')
    error = ''
    if request.method == 'POST':
        form = ConferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            error = 'Произошла ошибка. Данные конференции не отправлены.'
            logger.error(form.cleaned_data)
    else:
        form = ConferenceForm()
    
    context = {'form': form,
               'error': error}
    logger.debug(context)
    return render(request, 'main/conference.html', context)


def history(request):
    logger.info('Загрузка истории конференций. Шаблон: history.html')
    message = ''
    conferences_history = None
    qty_history = 0
    method = 1
    
    if request.method == 'POST':
        form = HistoryForm(request.POST)
        method = 0
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                conferences_history = Conference.objects.filter(Email=email)
                qty_history = len(conferences_history)
                if not qty_history:  # Если 0 конференций.
                    message = f'Для указанного email ({email}) в базе данных конференций не обнаружено.'
                    logger.info(message)
            except Exception as e:
                logger.error(f"Ошибка: {e}")
        
        else:
            logger.debug(f'Произошла ошибка. Данные конференции не отправлены. Данные формы: {form.cleaned_data}')
    else:
        form = HistoryForm()
    
    context = {'conferences_history': conferences_history,
               'qty_history': qty_history,
               'message': message,
               'method': method,
               'form': form}
    logger.debug(context)
    
    return render(request, 'main/history.html', context)


def faq(request):
    logger.info('Загрузка страницы с часто задаваемыми вопросами. Шаблон: faq.html')
    faqs = FAQ.objects.order_by('id')
    logger.debug(faqs)
    return render(request, 'main/faq.html', {'faqs': faqs})


def export(request):
    logger.info('Экспорт конференций.')
    try:
        conferences_queryset = Conference.objects.all()
        logger.debug(f'Кол-во загружаемых конференций: {len(conferences_queryset)}')
    except Exception as e:
        logger.exception(f'Загрузка конференций не удалась. Ошибка: {e}')
    
    output = write_to_excel(conferences_queryset)
    
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-conferences.xlsx"
    
    output.close()
    
    return response


def login_user(request):
    logger.info('Загрузка страницы входа на сайт.')
    if request.method == "POST":
        logger.debug('Загрузка login.html')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f'Вход на сайт пользователя {username}')
            return redirect('profile')
        else:
            messages.success(request, 'Произошла ошибка при авторизации... Просьба попробовать еще раз.')
            logger.warning(f"Неудачная попытка входа с логином: {username}")
            return redirect('login')
    else:
        return render(request, 'authentication/login.html')


def logout_user(request):
    logger.info('Загрузка страницы выхода с сайта.')
    logout(request)
    messages.success(request, 'Вы вышли из системы. Чтобы заново войти, заполните форму ниже.')
    return redirect('login')


@login_required
def profile(request):
    logger.info('Загрузка страницы профиля.')
    
    context = {'title': "Профиль"}

    return render(request, 'authentication/profile.html', context)


def vak(request):
    logger.info('Загрузка страницы добавления ВАК.')
    error = ''
    if request.method == 'POST':
        form = VAKForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Публикация добавлена!')
            return redirect('profile')
        else:
            error = 'Произошла ошибка. Данные публикации не отправлены.'
            logger.error(form.cleaned_data)
    else:
        form = VAKForm()
    
    context = {'title': "Добавление статьи ВАК",
               'form': form,
               'error': error}
    logger.debug(context)
    return render(request, 'authentication/vak.html', context)


def thesis(request):
    logger.info('Загрузка страницы добавления тезисов международных конференций.')
    error = ''
    if request.method == 'POST':
        form = ThesisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Публикация добавлена!')
            return redirect('profile')
        else:
            error = 'Произошла ошибка. Данные публикации не отправлены.'
            logger.error(form.cleaned_data)
    else:
        form = ThesisForm()

    context = {'title': "Добавление тезисов конференций",
               'form': form}
    logger.debug(context)
    return render(request, 'authentication/thesis.html', context)


@login_required
def edit(request, publication_id, type):
    logger.info('Загрузка страницы редактирования ВАК.')
    error = ''
    title = ''

    if type == 'vak':
        title = "Редактирование статьи ВАК"
        _queryset = VAK.objects.get(pk=publication_id)
    elif type == 'thesisWorld':
        title = 'Редактирование тезисов международных конференций'
        _queryset = Thesis.objects.get(pk=publication_id)
    elif type == 'thesisNation':
        title = 'Редактирование тезисов национальных конференций'
        _queryset = Thesis.objects.get(pk=publication_id)
        
    if request.method == 'POST':
        if type == 'vak':
            form = VAKForm(request.POST, instance=_queryset)
        elif type == 'thesisWorld' or type == 'thesisNation':
            form = ThesisForm(request.POST, instance=_queryset)
            
        if form.is_valid():
            form.save()
            messages.success(request, 'Публикация отредактирована!')
            return redirect('profile')
        else:
            error = 'Произошла ошибка. Данные публикации не отправлены.'
            logger.error(form.cleaned_data)
    else:
        # Словарь для заполнения формы
        initial = {}

        # vak_queryset = VAK.objects.get(pk=publication_id) # Получение данных из базы данных
        logger.debug(f'Загрузка публикации ВАК: {_queryset}')
        for key, value in _queryset.__dict__.items():
            if value:
                initial[key] = value
                # Для отображения в форме Института и кафедры:
                if key == 'IdInstitute_id':
                    initial['IdInstitute'] = value
                elif key == 'IdDeparture_id':
                    initial['IdDeparture'] = value
        logger.debug(f'Начальные данные: {initial}')

        if type == 'vak':
            form = VAKForm(initial=initial)
        elif type == 'thesisWorld' or type == 'thesisNation':
            form = ThesisForm(initial=initial)
    
    context = {'title': title,
               'type': type,
               'form': form,
               'error': error,
               'id': publication_id}
    logger.debug(context)
    return render(request, 'authentication/edit.html', context)


# Отчет по институтам
@login_required(redirect_field_name='login_user')
def main(request):
    institutes = Institute.objects.all()
    vaks = VAK.objects.filter(Accepted=True).values('IdInstitute__Name').annotate(sum=Sum('Points'))
    # https://docs.djangoproject.com/en/4.0/topics/db/aggregation/#following-relationships-backwards
    planVak = Institute.objects.annotate(total=Sum('departure__PlanVak'))
    
    thesisWorld = Thesis.objects.filter(Type='M').filter(Accepted=True).values('IdInstitute__Name').annotate(
        sum=Sum('Points'))
    planthesisWorld = Institute.objects.annotate(total=Sum('departure__PlanthesisWorld'))
    
    thesisNation = Thesis.objects.filter(Type='N').filter(Accepted=True).values('IdInstitute__Name').annotate(
        sum=Sum('Points'))
    planthesisNation = Institute.objects.annotate(total=Sum('departure__PlanthesisNation'))
    
    logger.debug(f'Vaks: {vaks}, тезисы в междун. конф: {thesisWorld}, тезисы в нац.конф: {thesisNation}')
    
    total_list = []  # Список для хранения списка Институтов

    for institute in institutes:
        # Преобразование информации по публикациям для отображения на сайте
        vak = get_publication('Количество публикаций в журналах ВАК', institute, planVak, vaks)
        tw = get_publication('Количество тезисов в международных конференциях', institute, planthesisWorld, thesisWorld)
        tn = get_publication('Количество тезисов в национальных конференциях', institute, planthesisNation, thesisNation)

        values = {
            'vak': vak,
            'thesisWorld': tw,
            'thesisNation': tn,
        }

        inst = DepartureTemplate(institute.id, f'{institute}', values)
        
        total_list.append(inst)
        
    context = {'title': "План-факт по науке",
               'total_list': total_list}
    logger.debug(context)
    return render(request, 'authentication/main.html', context)


# Функция для преобразования информации по публикациям
def get_publication(name, subdivision, planType, publicationType, type=0):
    
    # Плановый показатель
    plan = 0
    # planType есть только для институтов. Для кафедр считать иначе.
    if planType:
        for pt in planType:
            if pt == subdivision:
                plan = pt.total
    else:
        # Цифры от 1 до 3 означают Плна по статьям ВАК, Тезисам в междунар. или нац. конференциях соотвественно.
        if type == 1:
            plan = subdivision['PlanVak']
        elif type == 2:
            plan = subdivision['PlanthesisWorld']
        elif type == 3:
            plan = subdivision['PlanthesisNation']
            
    # Фактический показатель
    fact = 0
    for publication in publicationType:
        if isinstance(subdivision, Institute):
            if publication['IdInstitute__Name'] == f'{subdivision}':
                fact = publication['sum']
        elif isinstance(subdivision, dict): # TODO Разобраться почему Институты приходят как модель, а кафедры как словарь
            if publication['IdDeparture__Name'] == subdivision['Name']:
                fact = publication['sum']
                
    # Расчет % выполнения
    proc = 0
    if plan != 0:
        proc = round(fact / plan * 100, 2)
    
    data = {
        'name': name, # Название показателя
        'plan': plan,
        'fact': fact,
        'proc': proc,
    }
    return data


# Отчет по кафедрам для каждого института
@login_required
def report(request, institute_id):

    # Получение данных из соответствующих таблиц
    departures = Departure.objects.filter(IdInstitute=institute_id).values(
        'id', 'Name', 'PlanVak', 'PlanthesisWorld', 'PlanthesisNation')
    vaks = VAK.objects.filter(IdInstitute=institute_id).filter(Accepted=True).values('IdDeparture__Name').annotate(
        sum=Sum('Points'))
    thesisWorld = Thesis.objects.filter(Type='M').filter(Accepted=True).filter(IdInstitute=institute_id).values(
        'IdDeparture__Name').annotate(sum=Sum('Points'))
    thesisNation = Thesis.objects.filter(Type='N').filter(Accepted=True).filter(IdInstitute=institute_id).values(
        'IdDeparture__Name').annotate(sum=Sum('Points'))

    # Добавление в список кафедр необходимых параметров.
    total_list = []

    for departure in departures:
        # Преобразование информации по публикациям для отображения на сайте
        vak = get_publication('Количество публикаций в журналах ВАК', departure, False, vaks, 1)
        tw = get_publication('Количество тезисов в международных конференциях', departure, False, thesisWorld, 2)
        tn = get_publication('Количество тезисов в национальных конференциях', departure, False, thesisNation, 3)

        values = {
            'vak': vak,
            'thesisWorld': tw,
            'thesisNation': tn,
        }

        depart = DepartureTemplate(departure['id'], departure['Name'], values)
        total_list.append(depart)
 
    context = {'title': "План-факт по науке",
               'total_list': total_list}
    logger.debug(context)
    return render(request, 'authentication/report.html', context)


@login_required
def catalogue(request, department_id, type):
    title = "Список публикаций"
    publications = {}
    if type == 'vak':
        title = 'Список статей ВАК'
        publications = VAK.objects.filter(IdDeparture=department_id).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment')
    elif type == 'thesisWorld':
        title = 'Список тезисов международных конференций'
        publications = Thesis.objects.filter(IdDeparture=department_id).filter(Type='M').values(
            'id', 'Name', 'Accepted', 'Points', 'Comment', 'Type')
    elif type == 'thesisNation':
        title = 'Список тезисов национальных конференций'
        publications = Thesis.objects.filter(IdDeparture=department_id).filter(Type='N').values(
            'id', 'Name', 'Accepted', 'Points', 'Comment', 'Type')
        
    depart = Departure.objects.get(pk=department_id)

    context = {'title': title,
               'publications': publications,
               'depart': depart,
               'type': type}
    logger.debug(context)
    return render(request, 'authentication/catalogue.html', context)


def write_to_excel(conferences_queryset):
    # Определение заголовков.
    header_columns = [
        'Название конференции',
        'Страна',
        'Город',
        'Месяц',
        'Статус',
        'Общее число участников',
        'Кол-во представителей ГУУ',
        'Ссылка',
        'Email',
        'Студенческая',
        'Организатор ГУУ',
        'Общее число студентов',
        'Кол-во студентов из ГУУ',
        'Список приглашений',
        'Время создания записи',
    ]
    row_num = 0
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    workbook.remove_timezone = True
    worksheet = workbook.add_worksheet()
    # Определение ширины столбцов
    worksheet.set_column('A:A', 40)
    worksheet.set_column('B:D', 10)
    worksheet.set_column('E:E', 16)
    worksheet.set_column('F:F', 13)
    worksheet.set_column('G:I', 20)
    worksheet.set_column('J:L', 13)
    worksheet.set_column('M:M', 16)
    worksheet.set_column('N:O', 20)
    # Формат заголовков
    cell_format = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
    worksheet.set_row(0, cell_format=cell_format)
    # Запись заголовков
    for col_num, column_title in enumerate(header_columns, 0):
        worksheet.write(row_num, col_num, column_title)
    # Преобразования хранящихся данных из кортежа в словарь
    dict_month = dict_from_tuple(MONTH)
    dict_status = dict_from_tuple(STATUS)
    dict_country = dict_from_tuple(COUNTRY)
    # Последовательная запись конференций
    if conferences_queryset:
        for conference in conferences_queryset:
            row_num += 1
            
            # Поиск необходимых значеий в соответствующих словарях
            month = dict_month[conference.Month]
            country = dict_country[conference.Country]
            status = dict_status[conference.Status]
            student = binary(conference.Student)  # Студенческая или нет
            organizer = binary(conference.Organizer)  # Организатор ГУУ или нет
            
            timeCreate = conference.TimeCreate.strftime(
                "%d-%m-%Y %H:%M:%S")  # Преобразование времени в строковый формат
            
            # Определение значений для каждой строки
            row = [
                conference.Name,
                country,
                conference.City,
                month,
                status,
                conference.Total,
                conference.Delegate,
                conference.Url,
                conference.Email,
                student,
                organizer,
                conference.Total_student,
                conference.Delegate_student,
                conference.Invite,
                timeCreate,
            ]
            
            # Присвоение значений для каждой ячейки в строке
            for col_num, cell_value in enumerate(row, 0):
                worksheet.write(row_num, col_num, cell_value)
    workbook.close()
    output.seek(0)
    return output
