from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Institute, Conference, Employee, FAQ, VAK, Thesis, Departure, Monograph, Income, RID, Plan
from .forms import ConferenceForm, HistoryForm, VAKForm, ThesisForm, MonographForm, IncomeForm, RidForm
from django.http import HttpResponse
from datetime import datetime
from xlsxwriter.workbook import Workbook
import io
import logging
from .utils import dict_from_tuple, binary, MONTH, STATUS, COUNTRY, PARAMETERNAME, DepartureTemplate, send_mail_staff
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
import csv

logger = logging.getLogger(__name__)

BASE_FORMAT_PARAMS = {
    'text_wrap': True,
    'align': 'center',
    'valign': 'vcenter',
    'border': 1,
    'font_name': 'Times New Roman',
    'font_size': 12,
}

# Год по-умолчанию
Year_default = 2024  # Примечание: в файле menu.html жестко зафиксирован год по умолчанию в стр.39

# Названия показателей
_, Vak_name, Thes_M_name, Thes_N_name, Mono_name, Income_name, Rid_name = PARAMETERNAME


class VakListView(ListView):
   
    model = VAK
    paginate_by = 50
    
    def get_template_names(self):
        return 'main/publication_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список статей ВАК'
        context['model'] = 'vak'
        return context
    
    def get_ordering(self):
        return '-DateCreated'


class ThesisListView(ListView):
    model = Thesis
    paginate_by = 50
    
    def get_template_names(self):
        return 'main/publication_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список тезисов конференций'
        context['model'] = 'thesis'
        return context

    def get_ordering(self):
        return '-DateCreated'


class MonographListView(ListView):
    model = Monograph
    paginate_by = 50
    
    def get_template_names(self):
        return 'main/publication_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список монографий'
        context['model'] = 'monograph'
        return context

    def get_ordering(self):
        return '-DateCreated'
    

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
    
    context = {'title': "Профиль",
               'year': Year_default}

    return render(request, 'authentication/profile.html', context)


@login_required
def vak(request):
    logger.info('Загрузка страницы добавления ВАК.')

    # http://pythondjangorestapi.com/mastering-permissions-in-django-a-comprehensive-guide-to-secure-your-web-applications/
    deny = False
    if not request.user.has_perm('main.add_vak'):
        deny = True
        form = None
    else:
        if request.method == 'POST':
            form = VAKForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Публикация добавлена!')
                url = f"{request.scheme}://{request.META['HTTP_HOST']}/catalogue/{request.POST['IdDeparture']}/vak/{Year_default}"
                send_mail_staff(f'{form.cleaned_data["IdDeparture"]} добавила публикацию.',
                                url,
                                form.cleaned_data["IdDeparture"],
                                request.user.last_name,
                                )
                return redirect('profile')
            else:
                error = f'Произошла ошибка. Данные публикации не отправлены.{form.errors}'
                messages.error(request, error)
                logger.error(form.cleaned_data)
        else:
            form = VAKForm(initial={'Author': request.user})
        
    context = {'title': "Добавление статьи ВАК",
               'type': 'vak',
               'deny': deny,
               'form': form}
    logger.debug(context)
    return render(request, 'authentication/publication.html', context)


@login_required
def thesis(request):
    logger.info('Загрузка страницы добавления тезисов международных конференций.')

    deny = False
    if not request.user.has_perm('main.add_vak'):
        deny = True
        form = None
    else:
        if request.method == 'POST':
            form = ThesisForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Публикация добавлена!')
                form_type = 'thesisNation'
                if form.cleaned_data['Type'] == 'M':
                    form_type = 'thesisWorld'
                    
                url = f"{request.scheme}://{request.META['HTTP_HOST']}/catalogue/{request.POST['IdDeparture']}/{form_type}/{Year_default}"
                send_mail_staff(f'{form.cleaned_data["IdDeparture"]} добавила публикацию.',
                                url,
                                form.cleaned_data["IdDeparture"],
                                request.user.last_name,
                                )
                return redirect('profile')
            else:
                error = f'Произошла ошибка. Данные публикации не отправлены.{form.errors}'
                messages.error(request, error)
                logger.error(form.cleaned_data)
        else:
            form = ThesisForm(initial={'Author': request.user})

    context = {'title': "Добавление тезисов конференций",
               'type': 'thesis',
               'deny': deny,
               'form': form}
    logger.debug(context)
    return render(request, 'authentication/publication.html', context)


@login_required
def monograph(request):
    logger.info('Загрузка страницы добавления монографий.')

    deny = False
    if not request.user.has_perm('main.add_vak'):
        deny = True
        form = None
    else:

        if request.method == 'POST':
            form = MonographForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Монография добавлена!')
                url = f"{request.scheme}://{request.META['HTTP_HOST']}/catalogue/{request.POST['IdDeparture']}/monograph/{Year_default}"
                send_mail_staff(f'{form.cleaned_data["IdDeparture"]} добавила публикацию.',
                                url,
                                form.cleaned_data["IdDeparture"],
                                request.user.last_name,
                                )
                return redirect('profile')
            else:
                error = f'Произошла ошибка. Данные по монографии не отправлены. {form.errors}'
                messages.error(request, error)
                logger.error(form.cleaned_data)
        else:
            form = MonographForm(initial={'Author': request.user})
        
    context = {'title': "Добавление монографии",
               'type': 'monograph',
               'deny': deny,
               'form': form}
    logger.debug(context)
    return render(request, 'authentication/publication.html', context)


@login_required
def income(request):
    logger.info('Загрузка страницы добавления дохода')
    
    deny = False
    if not request.user.has_perm('main.add_income'):
        deny = True
        form = None
    else:
        
        if request.method == 'POST':
            form = IncomeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Доход по НИР добавлен!')
                url = f"{request.scheme}://{request.META['HTTP_HOST']}/catalogue/{request.POST['IdDeparture']}/income/{Year_default}"
                send_mail_staff(f'{form.cleaned_data["IdDeparture"]} добавил доход.',
                                url,
                                form.cleaned_data["IdDeparture"],
                                request.user.last_name,
                                )
                return redirect('profile')
            else:
                error = f'Произошла ошибка. Данные по доходу не отправлены. {form.errors}'
                messages.error(request, error)
                logger.error(form.cleaned_data)
        else:
            form = IncomeForm(initial={'Author': request.user})
    
    context = {'title': "Добавление дохода по НИР",
               'type': 'income',
               'deny': deny,
               'form': form,
               'year': Year_default}
    logger.debug(context)
    return render(request, 'authentication/publication.html', context)


@login_required
def rid(request):
    logger.info('Загрузка страницы добавления РИД')
    
    deny = False
    if not request.user.has_perm('main.add_rid'):
        deny = True
        form = None
    else:
        
        if request.method == 'POST':
            form = RidForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Доход по НИР добавлен!')
                url = f"{request.scheme}://{request.META['HTTP_HOST']}/catalogue/{request.POST['IdDeparture']}/rid/{Year_default}"
                send_mail_staff(f'{form.cleaned_data["IdDeparture"]} добавил РИД.',
                                url,
                                form.cleaned_data["IdDeparture"],
                                request.user.last_name,
                                )
                return redirect('profile')
            else:
                error = f'Произошла ошибка. Данные по РИД не отправлены. {form.errors}'
                messages.error(request, error)
                logger.error(form.cleaned_data)
        else:
            form = RidForm(initial={'Author': request.user})
    
    context = {'title': "Добавление РИД",
               'type': 'rid',
               'deny': deny,
               'form': form,
               'year': Year_default}
    logger.debug(context)
    return render(request, 'authentication/publication.html', context)


@login_required
def edit(request, publication_id, type):
    logger.info('Загрузка страницы редактирования записи')
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
    elif type == 'monograph':
        title = 'Редактирование монографии'
        _queryset = Monograph.objects.get(pk=publication_id)
    elif type == 'income':
        title = 'Редактирование НИР'
        _queryset = Income.objects.get(pk=publication_id)
    elif type == 'rid':
        title = 'Редактирование РИД'
        _queryset = RID.objects.get(pk=publication_id)
        
    if request.method == 'POST':
        if type == 'vak':
            form = VAKForm(request.POST, instance=_queryset)
        elif type == 'thesisWorld' or type == 'thesisNation':
            form = ThesisForm(request.POST, instance=_queryset)
        elif type == 'monograph':
            form = MonographForm(request.POST, instance=_queryset)
        elif type == 'income':
            form = IncomeForm(request.POST, instance=_queryset)
        elif type == 'rid':
            form = RidForm(request.POST, request.FILES, instance=_queryset)
            
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись отредактирована! Можете закрыть данную вкладку.')
            
            # Отправка письма только, если редактировал не админ.
            if not request.user.is_staff:
                send_mail_staff(f'{form.cleaned_data["IdDeparture"]} внесла изменения',
                                request.build_absolute_uri(),
                                form.cleaned_data["IdDeparture"],
                                request.user.last_name,
                                new=False)

            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            error = 'Произошла ошибка. Запись не изменена.'
            logger.error(form.cleaned_data)
    else:
        # Словарь для заполнения формы
        initial = {}

        logger.debug(f'Загрузка записи: {_queryset}')
        for key, value in _queryset.__dict__.items():
            if value:
                initial[key] = value
                # Для отображения названия кафедры:
                if key == 'IdDeparture_id':
                    initial['IdDeparture'] = value
                elif key == 'Author_id':
                    initial['Author'] = value
        logger.debug(f'Начальные данные: {initial}')

        if type == 'vak':
            form = VAKForm(initial=initial)
        elif type == 'thesisWorld' or type == 'thesisNation':
            form = ThesisForm(initial=initial)
        elif type == 'monograph':
            form = MonographForm(initial=initial)
        elif type == 'income':
            form = IncomeForm(initial=initial)
        elif type == 'rid':
            form = RidForm(initial=initial)
    
    context = {'title': title,
               'type': type,
               'form': form,
               'error': error,
               'id': publication_id}
    logger.debug(context)
    return render(request, 'authentication/edit.html', context)


# Отчет по институтам
@login_required(redirect_field_name='login_user')
def main(request, year=Year_default):
    total_list = get_info_institute(year)

    context = {'title': "План-факт по науке",
               'total_list': total_list,
               'year': year}
    logger.debug(context)
    return render(request, 'authentication/main.html', context)


@login_required(redirect_field_name='login_user')
def old(request, year):
    total_list = get_info_institute(year)

    context = {'title': "План-факт по науке",
               'total_list': total_list,
               'year': year}
    logger.debug(context)
    return render(request, 'authentication/main.html', context)


def get_info_institute(year):
    institutes = Institute.objects.all()

    total_list = []  # Список для хранения списка Институтов
    for institute in institutes:
        # Преобразование информации по публикациям для отображения на сайте
        vak = get_publication(Vak_name, institute.id, year)
        tw = get_publication(Thes_M_name, institute.id, year)
        tn = get_publication(Thes_N_name, institute.id, year)
        mo = get_publication(Mono_name, institute.id, year)
        
        income = get_publication(Income_name, institute.id, year)
        rid = get_publication(Rid_name, institute.id, year)
        
        values = {
            'vak': vak,
            'thesisWorld': tw,
            'thesisNation': tn,
            'monograph': mo,
            'income': income,
            'rid': rid
        }
        
        inst = DepartureTemplate(institute.id, f'{institute}', values)
        
        total_list.append(inst)
    return total_list


def get_publication(name, id, year, type=True):
    '''
    Функция для преобразования информации по публикациям
    
    :param name: tuple, Название показателя ('ВАК', 'Количество публикаций в журналах ВАК')
    :param id: ID Института или кафедры
    :param year: Год отчета
    :param type: Флаг для определния типа подразделения. Если True, то Институт. Если False - кафедра

    
    :return: dict,
        data = {
            'name': name[1], # Название показателя хранится во втором элементе tuple
            'plan': plan,
            'fact': fact,
            'proc': proc,
        }
    '''

    plan = get_plan(name[0], id, year, type)
    fact = get_fact(name[0], id, year, type)

    proc = get_proc(fact, plan)

    data = {
        'name': name[1],
        'plan': plan,
        'fact': fact,
        'proc': proc,
    }
    return data


# Отчет по кафедрам для каждого института
@login_required
def report(request, institute_id, year):

    total_list = get_info_departure(institute_id, year)

    context = {'title': "План-факт по науке",
               'total_list': total_list,
               'institute_id': institute_id,
               'year': Year_default}
    logger.debug(context)
    return render(request, 'authentication/report.html', context)


def get_info_departure(institute_id, year):
    # Получение данных из соответствующих таблиц
    departures = Departure.objects.filter(IdInstitute=institute_id).values('id', 'Name')

    # Добавление в список кафедр необходимых параметров.
    total_list = []
    for departure in departures:
        # Преобразование информации по публикациям для отображения на сайте
        vak = get_publication(Vak_name, departure['id'], year, type=False)
        tw = get_publication(Thes_M_name, departure['id'], year, type=False)
        tn = get_publication(Thes_N_name, departure['id'], year, type=False)
        mo = get_publication(Mono_name, departure['id'], year, type=False)
        income = get_publication(Income_name, departure['id'], year, type=False)
        rid = get_publication(Rid_name, departure['id'], year, type=False)
        
        values = {
            'vak': vak,
            'thesisWorld': tw,
            'thesisNation': tn,
            'monograph': mo,
            'income': income,
            'rid': rid
        }
        
        depart = DepartureTemplate(departure['id'], departure['Name'], values)
        total_list.append(depart)
    return total_list


@login_required
def catalogue(request, department_id, type, year):
    title = "Список публикаций"
    publications = {}
    if type == 'vak':
        title = 'Список статей ВАК'
        publications = VAK.objects.filter(IdDeparture=department_id, Year=year).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment')
    elif type == 'thesisWorld':
        title = 'Список тезисов международных конференций'
        publications = Thesis.objects.filter(IdDeparture=department_id, Type='M', Year=year).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment', 'Type')
    elif type == 'thesisNation':
        title = 'Список тезисов национальных конференций'
        publications = Thesis.objects.filter(IdDeparture=department_id, Type='N', Year=year).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment', 'Type')
    elif type == 'monograph':
        title = 'Список монографий'
        publications = Monograph.objects.filter(IdDeparture=department_id, Year=year).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment')
    elif type == 'income':
        title = 'Список НИР'
        publications = Income.objects.filter(IdDeparture=department_id, Year=year).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment')
    elif type == 'rid':
        title = 'Список РИД'
        publications = RID.objects.filter(IdDeparture=department_id, Year=year).values(
            'id', 'Name', 'Accepted', 'Points', 'Comment')
        
    depart = Departure.objects.get(pk=department_id)

    context = {'title': title,
               'publications': publications,
               'depart': depart,
               'type': type,
               'year': year}
    logger.debug(context)
    return render(request, 'authentication/catalogue.html', context)


# Расчет процента выполнения плана
def get_proc(fact, plan):
    # Расчет % выполнения
    proc = 0
    if plan != 0:
        proc = round(fact / plan * 100, 2)
    return proc


def get_plan(name: str, id: int, year: int, type: bool) -> float:
    '''
    Функция для получения планового показателя для кафедры или Института
    
    :param name: Названиение показателя (Значения: 'ВАК', 'ТЕЗИСЫ_М', 'ТЕЗИСЫ_Н', 'МОНОГРАФИЯ', 'ДОХОД', 'РИД')
    :param id: ID института или кафедры
    :param year: Год показателя
    :param type: Флаг для определния типа подразделения. Если True, то Институт. Если False - кафедра
    :return: Значение показателя
    '''


    if type:
        v = Plan.objects.filter(Departure__IdInstitute=id, Name=name, Year=year).aggregate(Sum("Value", default=0))
        if v:
            return v['Value__sum']
        else: # Если пустой Queryset
            return 0.0
    
    else:
        v = Plan.objects.filter(Departure=id, Name=name, Year=year)
        if v: # Если пустой Queryset
            return v[0].Value
        else:
            return 0.0


def get_fact(name: str, id: int, year: int, type: bool) -> float:
    '''
    
    :param name: Название показателя (Значения: 'ВАК', 'ТЕЗИСЫ_М', 'ТЕЗИСЫ_Н', 'МОНОГРАФИЯ', 'ДОХОД', 'РИД')
    :param id: ID института или кафедры
    :param year: Год показателя
    :param type: Флаг для определния типа подразделения. Если True, то Институт. Если False - кафедра
    :return: Значение показателя
    '''

    if type:

        if name == "ВАК":
            res = VAK.objects.filter(Accepted=True, IdDeparture__IdInstitute=id, Year=year)
        elif name == "ТЕЗИСЫ_М":
            res = Thesis.objects.filter(Accepted=True, IdDeparture__IdInstitute=id, Type='M', Year=year)
        elif name == "ТЕЗИСЫ_Н":
            res = Thesis.objects.filter(Accepted=True, IdDeparture__IdInstitute=id, Type='N', Year=year)
        elif name == "МОНОГРАФИЯ":
            res = Monograph.objects.filter(Accepted=True, IdDeparture__IdInstitute=id, Year=year)
        elif name == 'ДОХОД':
            res = Income.objects.filter(Accepted=True, IdDeparture__IdInstitute=id, Year=year)
        elif name == 'РИД':
            res = RID.objects.filter(Accepted=True, IdDeparture__IdInstitute=id, Year=year)
            
    else:
        if name == "ВАК":
            res = VAK.objects.filter(Accepted=True, IdDeparture=id, Year=year)
        elif name == "ТЕЗИСЫ_М":
            res = Thesis.objects.filter(Accepted=True, IdDeparture=id, Type='M', Year=year)
        elif name == "ТЕЗИСЫ_Н":
            res = Thesis.objects.filter(Accepted=True, IdDeparture=id, Type='N', Year=year)
        elif name == "МОНОГРАФИЯ":
            res = Monograph.objects.filter(Accepted=True, IdDeparture=id, Year=year)
        elif name == 'ДОХОД':
            res = Income.objects.filter(Accepted=True, IdDeparture=id, Year=year)
        elif name == 'РИД':
            res = RID.objects.filter(Accepted=True, IdDeparture=id, Year=year)
        
    if res:
        fact = res.aggregate(sum=Sum('Points'))['sum']
    else:  # Если пустой Queryset
        fact = 0.0
        
    return fact
    

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


@login_required
def export_pf_all(request, year):
    logger.info('Экспорт План-факта Университета')
    
    objects_institutes = Institute.objects.all()
    
    dict_info = {}
    for ins in objects_institutes:
        info = get_info_departure(ins.id, year)
        dict_info[ins.Name] = info

    output = plan_fact_to_excel(dict_info)

    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-plan_fact.xlsx"

    output.close()

    return response


@login_required
def export_pf(request, institute_id, year):

    ins = Institute.objects.get(id=institute_id)
    logger.info(f'Экспорт План-факта {ins}')
    
    dict_info = {}
    info = get_info_departure(ins.id, year=year)
    dict_info[ins.Name] = info

    output = plan_fact_to_excel(dict_info)
    
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-plan_fact-{ins.id}.xlsx"

    output.close()

    return response


def plan_fact_to_excel(data):

    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    workbook.remove_timezone = True
    worksheet = workbook.add_worksheet()
    _format = workbook.add_format(BASE_FORMAT_PARAMS)
    write_headers(worksheet, _format)

    row_num = 2
    col_num = 0
    col_finish = 18
    
    for name, values in data.items():

        worksheet.merge_range(row_num, col_num, row_num, col_finish, name)
        row_num += 1
        for department in values:
            worksheet.write(row_num, col_num, department.name)
    
            parameter_list = ['vak', 'thesisWorld', 'thesisNation', 'monograph', 'income', 'rid']
            col_list = ['plan', 'fact', 'proc']
            col_start = 1
            
            for parameter in parameter_list:
                for col in col_list:
                    worksheet.write(row_num, col_start, department.values[parameter][col], _format)
                    col_start += 1
            row_num += 1
        
    workbook.close()
    output.seek(0)
    return output


# Запись заголовков для план-факта
def write_headers(worksheet, header_format):

    worksheet.merge_range('A1:A2', 'Структурное подразделение', header_format)
    worksheet.set_column('A:A', 80)
    worksheet.set_row(0, 50)
    worksheet.merge_range('B1:D1', 'Публикации ВАК, шт.', header_format)
    worksheet.set_column('B1:D1', 10)
    worksheet.merge_range('E1:G1', 'Тезисы докладов на международных конференциях, шт.', header_format)
    worksheet.merge_range('H1:J1', 'Тезисы докладов на национальных  конференциях, шт.', header_format)
    worksheet.merge_range('K1:M1', 'Монографии', header_format)
    worksheet.merge_range('N1:P1', 'Доход, руб.', header_format)
    worksheet.set_column('N:O', 15)
    worksheet.merge_range('Q1:S1', 'РИД/Патент', header_format)

    row_num = 1
    col_start = 1
    col_finish = 17
    _list = ['План', 'Факт', '% Выпол.']
    for cell_value in _list:
        for col_num in range(col_start, col_finish, 3):
            worksheet.write(row_num, col_num, cell_value, header_format)
        col_start += 1
        col_finish += 1


# Экспорт публикаций в csv-формат
# https://docs.djangoproject.com/en/4.1/howto/outputting-csv/
def export_publications_csv(request, model):
    
    # Базовые поля, используемые в файле csv
    base_fields = ['id', 'Name', 'Output', 'Year', 'Pages', 'DepartmentSame', 'DepartmentOther', 'Url',
                   'IdDeparture__Name', 'Accepted', 'Points', 'Comment', 'DateCreated']
    
    # Для тезисов добавляется поле с Типом (Международная/Национальная)
    thesis_fields = base_fields.copy()
    thesis_fields.append('Type')

    # Заголовки для файла с ВАК
    base_list_name = ['№', 'Название публикации', 'Название журнала', 'Год', 'Страницы', 'Авторы c отчетной кафедры',
                      'Авторы с других кафедр', 'Ссылка', 'Кафедра', 'Принято', 'Кол-во баллов', 'Комментарий', 'Дата внесения']
    
    # Заголовки и поля для файла с тезисами
    # Добавление столбца с Типом конференции и изменение одного из существующих
    thesis_list_name = base_list_name.copy()
    thesis_list_name.append('Тип конференции')
    thesis_list_name[1] = 'Название конференции'
    
    # Заголовки для файла с монографиями
    # Изменения одного из существующих
    monograph_list_name = base_list_name.copy()
    monograph_list_name[0] = 'Название монографии'
    monograph_list_name[1] = 'ISBN'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-list_{model}.csv"

    writer = csv.writer(response, delimiter=';')

    if model == 'vak':  # Для ВАК
        writer.writerow(['Список публикаций ВАК'])
    
        writer.writerow(base_list_name)
    
        publications = VAK.objects.all().values_list(*base_fields)
    elif model == 'thesis':  # Для тезисов
        writer.writerow(['Список тезисов конференций'])

        writer.writerow(thesis_list_name)

        publications = Thesis.objects.all().values_list(*thesis_fields)
        
    elif model == 'monograph':  # Для монографий
        writer.writerow(['Список монографий'])

        writer.writerow(monograph_list_name)

        publications = Monograph.objects.all().values_list(*base_fields)
    else:
        publications = []
        logger.error(f'Отсутствует модель публикаций для экспорта в csv для модели {model}')

    for publication in publications:
        writer.writerow(publication)
    return response

    
class PassChangeView(PasswordChangeView):
    template_name = 'authentication/password_change.html'
    extra_context = {'title': 'Смена пароля'}
    

class PassChangeDoneView(PasswordChangeDoneView):
    template_name = 'authentication/password_change_done.html'
    extra_context = {'message': 'Вы изменили пароль!'}