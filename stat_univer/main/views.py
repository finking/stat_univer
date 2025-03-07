from abc import abstractmethod

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LoginView
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, FormView, UpdateView

import io
import logging
from datetime import datetime
from xlsxwriter.workbook import Workbook

from .forms import ConferenceForm, HistoryForm, VAKForm, ThesisForm, MonographForm, IncomeForm, RidForm, DashboardForm
from .models import Institute, Conference, FAQ, VAK, Thesis, Departure, Monograph, Income, RID, Plan
from .utils import PARAMETERNAME, send_mail_staff


logger = logging.getLogger(__name__)

# Названия показателей
_, Vak_name, Thes_M_name, Thes_N_name, Mono_name, Income_name, Rid_name = PARAMETERNAME

# Словарь для связи названий показателей с функциями получения фактических данных
FACT_FUNCTIONS = {
    'ВАК': ['Количество публикаций в журналах ВАК', 'get_fact_vak', 'vak_list_departure'],
    'ТЕЗИСЫ_М': ['Количество тезисов в международных конференциях', 'get_fact_thesis', 'thesis_list_departure'],
    'ТЕЗИСЫ_Н': ['Количество тезисов в национальных конференциях', 'get_fact_thesis', 'thesis_list_departure'],
    'МОНОГРАФИЯ': ['Количество монографий', 'get_fact_monograph', 'monograph_list_departure'],
    'ДОХОД': ['Общий доход, руб.', 'get_fact_income', 'income_list_departure'],
    'РИД': ['РИД','get_fact_rid', 'rid_list_departure'],
}

# Базовый формат для записи в excel-файл
BASE_FORMAT_PARAMS = {
    'text_wrap': True,
    'align': 'center',
    'valign': 'vcenter',
    'border': 1,
    'font_name': 'Times New Roman',
    'font_size': 12,

}
# Год по-умолчанию берется из 'main.context_processors.current_year'


class LoginUser(LoginView):
    template_name = 'authentication/login.html'
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка при авторизации... Просьба попробовать еще раз.")
        username = self.request.POST['username']
        logger.warning(f"Неудачная попытка входа с логином: {username}")
        return super().form_invalid(form)


class PassChangeView(PasswordChangeView):
    template_name = 'authentication/password_change.html'
    extra_context = {'title': 'Смена пароля'}


class PassChangeDoneView(PasswordChangeDoneView):
    template_name = 'authentication/password_change_done.html'
    extra_context = {'message': 'Вы изменили пароль!'}


# Класс для отображения визуальной информации
class DashboardView(FormView):
    form_class = DashboardForm
    template_name = 'main/dashboard.html'
    initial_feature = ('ВАК', 'Количество публикаций в журналах ВАК')
    initial = {'feature': initial_feature[0]}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']  # Получаем год из URL
        context['year'] = year
        context['title'] = f"План-факт по науке за {year} год"
        context['feature'] = self.initial_feature[1]
        context['objects'] = self.get_institute_proc(year)
        
        return context

    def form_valid(self, form):
        feature = form.cleaned_data['feature']  # Получение наименования Показателя из формы.
        dict_parameter = dict(PARAMETERNAME)  # Преобразование кортежа с параметрами в словарь
    
        # Элемент словаря - это кортеж, н-р ('ВАК', 'Количество публикаций в журналах ВАК')
        for parameter in dict_parameter:
            if feature in parameter:
                # Если Показатель найден, то присваиваем начальные значения для Form в виде:
                # Ключа ('ВАК') и Значения ('Количество публикаций в журналах ВАК')
                self.initial_feature = (feature, dict_parameter[parameter])
                break
    
        context = self.get_context_data()
        context['objects'] = self.get_institute_proc(year=context['year'])
    
        return self.render_to_response(context)
    
    def get_institute_proc(self, year: int) -> dict:
        """ Возвращает словарь, хранящий пары {Институт: процент выполнения плана}"""
        dict_data = {}
        institutes = Institute.objects.all()
        for institute in institutes:
            proc = self.get_proc(institute, year, self.initial_feature[0])
            dict_data[institute.ShortName] = proc
        return dict_data
    
    @staticmethod
    def get_proc(institute: Institute, year: int, indicator: str) -> float:
        """
        Метод для получения процента выполнения плана для конкретного института
        
        :param institute: Объект модели Institute
        :param year: Отчетный год
        :param indicator: Название индикатора (например, ВАК)
        :return: Процент выполнения плана
        """
        
        # Получение планового значения
        plan = 0.0
        queryset = Plan.objects.filter(
            Departure__Institute=institute.id, Name=indicator, Year=year).aggregate(Sum("Value", default=0))
        if queryset:
            plan = queryset['Value__sum']
        
        # Получение фактического значения (частный случай метода get_institute_plan_fact класса InstituteReportListView)
        fact = 0.0
        departures = Departure.objects.filter(Institute=institute)
        for departure in departures:
            array = FACT_FUNCTIONS[indicator]
            fact_function_name = array[1]  # Имя функции для расчета фактических данных
            fact_function = getattr(departure, fact_function_name)  # Функция для расчета фактических данных
            fact_value = fact_function(year)
            if fact_value:
                fact += fact_value
        
        return fact / plan * 100 if plan else 0.0
    
    
# Главная страница
class Index(TemplateView):
    template_name = 'main/index.html'


# Страница профиля
class ProfileView(TemplateView, LoginRequiredMixin):
    template_name = 'authentication/profile.html'
    extra_context = {'title': "Профиль"}


# Список Институтов с Директорами и их заместителями
class InstituteList(ListView):
    model = Institute
    template_name = 'main/institute.html'
    context_object_name = 'institutes'
    extra_context = {'title': 'Институты ГУУ'}
    ordering = ['-id']


# Страница с часто задаваемыми вопросами
class FaqView(ListView):
    model = FAQ
    template_name = 'main/faq.html'
    context_object_name = 'faqs'


# Заполнение формы по конференциям
class ConferenceView(CreateView):
    template_name = 'main/conference.html'
    form_class = ConferenceForm
    success_url = 'conference'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные добавлены! Можете внести новую информацию.')
        return super().form_valid(form)


# Отображение внесенных конференций (по email сотрудника, которых их вносил)
class HistoryView(FormView):
    template_name = 'main/history.html'
    form_class = HistoryForm
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        conferences_history = Conference.objects.filter(Email=email)
        context = {'conferences_history': conferences_history,
                   'form': form}
        return self.render_to_response(context)


# Общий класс для CreateView публикаций, дохода и РИД
class GeneralCreateView(CreateView, LoginRequiredMixin):
    template_name = 'authentication/create.html'
    success_url = 'profile'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['Author'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные добавлены!')
        send_mail_staff(form.cleaned_data["Name"],
                        f"{self.request.scheme}://{self.request.META['HTTP_HOST']}{self.request.path}/update/{form.instance.id}",
                        form.cleaned_data["Departure"],
                        self.request.user.last_name,
                        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error('Форма недействительна: %s', form.errors)
        error = f'Произошла ошибка. Данные публикации не отправлены.{form.errors}'
        messages.error(self.request, error)
        return super().form_invalid(form)


class VakCreateView(PermissionRequiredMixin, GeneralCreateView):
    model = VAK
    form_class = VAKForm
    permission_required = 'main.add_vak'
    
    extra_context = {
        'title': "Добавление статьи ВАК",
    }


class ThesisCreateView(PermissionRequiredMixin, GeneralCreateView):
    model = Thesis
    form_class = ThesisForm
    permission_required = 'main.add_thesis'
    
    extra_context = {
        'title': "Добавление публикации на конференции",
        'feature': 'thesis'
    }


class MonographCreateView(PermissionRequiredMixin, GeneralCreateView):
    model = Monograph
    form_class = MonographForm
    permission_required = 'main.add_monograph'
    
    extra_context = {
        'title': "Добавление монографии",
    }


class IncomeCreateView(PermissionRequiredMixin, GeneralCreateView):
    model = Income
    form_class = IncomeForm
    permission_required = 'main.add_income'
    
    extra_context = {
        'title': "Добавление дохода по НИР",
    }


class RidCreateView(PermissionRequiredMixin, GeneralCreateView):
    model = RID
    form_class = RidForm
    permission_required = 'main.add_rid'
    
    extra_context = {
        'title': "Добавление РИД",
    }


# Общий класс для UpdateView публикаций, дохода и РИД
class GeneralEditView(UpdateView, LoginRequiredMixin):
    extra_context = {
        'title': "Редактирование записи",
    }
    
    template_name = 'authentication/edit.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Запись отредактирована! Можете закрыть данную вкладку.')
        if not self.request.user.is_staff:
            send_mail_staff(
                form.cleaned_data["Name"],
                self.request.build_absolute_uri(),
                form.cleaned_data["Departure"],
                self.request.user.last_name,
                new=False)
        
        return super().form_valid(form)


class VakEditView(PermissionRequiredMixin, GeneralEditView):
    model = VAK
    form_class = VAKForm
    permission_required = 'main.change_vak'


class ThesisEditView(PermissionRequiredMixin, GeneralEditView):
    model = Thesis
    form_class = ThesisForm
    permission_required = 'main.change_thesis'


class MonographEditView(PermissionRequiredMixin, GeneralEditView):
    model = Monograph
    form_class = MonographForm
    permission_required = 'main.change_monograph'


class IncomeEditView(PermissionRequiredMixin, GeneralEditView):
    model = Income
    form_class = IncomeForm
    permission_required = 'main.change_income'


class RidEditView(PermissionRequiredMixin, GeneralEditView):
    model = RID
    form_class = RidForm
    permission_required = 'main.change_rid'


# Класс отображения план-факта Университета (всех Институтов)
class InstituteReportListView(ListView):
    model = Institute
    template_name = 'authentication/institute_report_list.html'
    context_object_name = 'institutes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']  # Получаем год из URL
        context['year'] = year
        context['title'] = "План-факт по науке"
        
        # Для каждого института получаем данные
        for institute in context['institutes']:  # Хранится в context['institutes'], плагодаря context_object_name
            institute.report_data = self.get_institute_plan_fact(institute.id, year)
        
        return context
    
    # Функция для получения план-факта института
    @staticmethod
    def get_institute_plan_fact(institute_id: int, year: int) -> dict:
        """
        Метод для получения плановых и фактических значений для конкетного института
        
        :param institute_id: ID Института
        :param year: отчетный год
        :return: Словарь со значениями {
            'institute': institute.Name,
            'total': {
            'indicator': ['Name_parameter', plan, fact, proc]
            },
        }
        """
        # Получаем институт
        institute = Institute.objects.get(id=institute_id)
        
        # Получаем все кафедры, относящиеся к институту
        departures = Departure.objects.filter(Institute=institute)
        
        # Словарь для хранения итоговых данных
        result = {
            'institute': institute.Name,
            'total': {},
        }
        
        for indicator, array in FACT_FUNCTIONS.items():
            # Получаем план для данного параметра
            plan = 0.0
            queryset = Plan.objects.filter(
                Departure__Institute=institute_id, Name=indicator, Year=year).aggregate(Sum("Value", default=0))
            if queryset:
                plan = queryset['Value__sum']
            
            # Инициализируем массив значений для каждого показателя
            # Название параметра (например, ВАК), план, факт, процент выполнения
            result['total'][indicator] = [array[0], plan, 0, 0]
        
        # Обрабатываем каждую кафедру
        for departure in departures:
            # FACT_FUNCTIONS имеет вид 'ВАК': ['Количество публикаций в журналах ВАК', 'get_fact_vak']
            for indicator, array in FACT_FUNCTIONS.items():
                fact_function_name = array[1]  # Имя функции для расчета фактических данных
                fact_function = getattr(departure, fact_function_name)  # Функция для расчета фактических данных
                
                # Вызываем функцию и получаем фактические данные
                fact_value = fact_function(year)
                if fact_value:
                    result['total'][indicator][2] += fact_value  # Записываем в третий "слот" result (факт)
        
        # Записываем во четвертый "слот" result (процент выполн) по каждому показателю
        for indicator in FACT_FUNCTIONS.keys():
            result['total'][indicator][3] = result['total'][indicator][2] / result['total'][indicator][1] * 100 \
                if result['total'][indicator][1] != 0 else 0
        logger.debug(result)
        return result


class DepartmentReportMixin:
    @staticmethod
    def get_departure_plan_fact(departure: Departure, year: int) -> dict:
        """
        Метод для получения плановых и фактических значений для конкетного института
        
        :param departure: Объект модели Departure
        :param year:
        :return: Словарь со значениями {
            'institute': institute.Name,
            'total': {
                'indicator': {'Name_parameter':
                                    {plan: value},
                                    {fact: value},
                                    {proc: value},
                            },
            }}
        """
        
        # Словарь для хранения итоговых данных
        result = {
            'departure_name': departure.Name,
            'total': {},
        }
        
        for indicator, array in FACT_FUNCTIONS.items():
            indicator_name, fact_function_name, url_name = array
            
            # Получаем план по показателю, если он имеется.
            plan = 0.0
            try:
                plan = Plan.objects.get(Departure=departure.id, Name=indicator, Year=year).Value
            except Plan.DoesNotExist:
                pass
            
            fact = getattr(departure, fact_function_name)(year) if indicator != "ТЕЗИСЫ_Н" else \
                getattr(departure, fact_function_name)(year, "N")
            if not fact:
                fact = 0.0
            
            proc = fact / plan * 100 if plan else 0.0
            
            url = reverse(url_name, kwargs={'department_id': departure.id, 'year': year})
            
            # Инициализируем словарь значений для каждого показателя
            # Название параметра (например, ВАК), план, факт, процент выполнения
            result['total'][indicator_name] = {'plan': plan,
                                               'fact': fact,
                                               'proc': proc,
                                               'url': url}
        
        return result


# Класс отображения план-факта Института (по кафедрам)
class DepartmentReportListView(DepartmentReportMixin, TemplateView):
    template_name = 'authentication/departure_report_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        context['year'] = year
        context['title'] = 'План-факт по науке'
        institute_id = self.kwargs.get('institute_id')  # Получаем id института из url
        context['institute_id'] = institute_id
        
        departures_list = [] # Список кафедр со значениями
        deps = Departure.objects.filter(Institute_id=institute_id)
        # Для каждой кафедры получаем данные
        for departure in deps:
            departures_list.append(self.get_departure_plan_fact(departure, year))
        
        context['departures_list'] = departures_list
        return context


# Общий миксин для отображения списков публикаций
class PublicationMixin:
    template_name = 'main/publication_list.html'
    paginate_by = 50
    ordering = '-DateCreated'


# Список статей ВАК всего университета
class VakListView(PublicationMixin, ListView):
    model = VAK
    extra_context = {
        'title': 'Список статей ВАК',
        'model': 'vak'
    }


# Список тезисов конференций всего университета
class ThesisListView(PublicationMixin, ListView):
    model = Thesis
    extra_context = {
        'title': 'Список тезисов конференций',
        'model': 'thesis'
    }
    

# Список монографий всего университета
class MonographListView(PublicationMixin, ListView):
    model = Monograph
    extra_context = {
        'title': 'Список монографий',
        'model': 'monograph'
    }


# Миксин для отображения списков конкретной кафедры
class ListDepartureMixin:
    template_name = 'authentication/department_parametr_list.html'
    # context_object_name = 'departures'
    ordering = ['-Year', '-DateCreated']
    paginate_by = 10
    
    def get_queryset(self):
        department_id = self.kwargs.get('department_id')  # Получаем id кафедры из url
        return super().get_queryset().filter(Departure=department_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature'] = self.kwargs.get('feature')  # Передача типа параметра (например, ВАК)
        context['year'] = self.kwargs.get('year')
        context['departure'] = Departure.objects.get(id=self.kwargs.get('department_id'))
        return context


# Список публикаций ВАК конкретной кафедры
class VakListDepartureView(ListDepartureMixin, ListView):
    model = VAK

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список статей ВАК'
        context['feature'] = 'vak'
        return context


# Список тезисов конкретной кафедры
class ThesisListDepartureView(ListDepartureMixin, ListView):
    model = Thesis

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список тезисов конференций'
        context['feature'] = 'thesis'
        return context


# Список монографий конкретной кафедры
class MonographListDepartureView(ListDepartureMixin, ListView):
    model = Monograph

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список монографий'
        context['feature'] = 'monograph'
        return context


# Список дохода конкретной кафедры
class IncomeListDepartureView(ListDepartureMixin, ListView):
    model = Income
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список НИР'
        context['feature'] = 'income'
        return context


# Список РИД конкретной кафедры
class RidListDepartureView(ListDepartureMixin, ListView):
    model = RID
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список РИД'
        context['feature'] = 'rid'
        return context
    
    
# Базовый класс для записи в Excel-файл
class ExcelWriterBase:
    def __init__(self, request, queryset, offset=1, header_columns=None, top_headers=None, sub_headers=None, width_colunms=None,
                 year=None):
        self.request = request
        self.queryset = queryset
        self.offset = offset
        self.header_columns = header_columns
        self.sub_headers = sub_headers
        self.top_headers = top_headers
        self.width_colunms = width_colunms
        self.year = year
        self.lst = []
        
    # Создание заголовков
    def create_headers(self, workbook, worksheet):
        # Формат заголовков
        cell_format = workbook.add_format(BASE_FORMAT_PARAMS)
        worksheet.set_row(0, cell_format=cell_format)
        
        # Запись заголовков
        for col_num, column_title in enumerate(self.header_columns):
            worksheet.write(0, col_num, column_title, cell_format)
    
    # Устаровка ширины для столбцов
    def set_column_widths(self, worksheet):
        for ws in self.width_colunms:
            worksheet.set_column(*ws)

    # Формирование строк для записи в файл
    @abstractmethod
    def get_rows(self):
        pass

    # Запись данных
    def write_data(self, worksheet):
        if self.request.user.is_authenticated:
            for row_num, row in enumerate(self.lst):
                for col_num, cell_value in enumerate(row):
                    worksheet.write(row_num+self.offset, col_num, cell_value)
        else:
            worksheet.write(self.offset, 0,
                            'Чтобы увидеть здесь данные, необходимо войти в систему и иметь соответствующие права...')
            
    # Генерация файла
    def generate_excel(self):
        # Инициализация файла Excel
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        
        # Вызов методов для настройки таблицы
        self.set_column_widths(worksheet)
        self.create_headers(workbook, worksheet)
        self.get_rows()
        self.write_data(worksheet)
        
        # Закрытие книги и возврат байтового потока
        workbook.close()
        output.seek(0)
        return output
    
    
# Класс для записи конференций в Excel-файл
class ExcelWriterConference(ExcelWriterBase):
    
    # Формирование строк для записи в файл
    def get_rows(self):
        for conference in self.queryset:
            row = [
                conference.Name,
                conference.get_Country_display(),
                conference.City,
                conference.get_Month_display(),
                conference.get_Status_display(),
                conference.Total,
                conference.Delegate,
                conference.Url,
                conference.Email,
                conference.get_student_display(),
                conference.get_organizer_display(),
                conference.Total_student,
                conference.Delegate_student,
                conference.Invite,
                conference.get_timeCreate()
            ]
            self.lst.append(row)


# Класс для записи публикаций в Excel-файл
class ExcelWriterPublication(ExcelWriterBase):
    # Формирование строк для записи в файл
    def get_rows(self):
        for q in self.queryset:
            row = [q.id,
                   q.Name,
                   q.Output,
                   q.Year,
                   q.Pages,
                   q.DepartmentSame,
                   q.DepartmentOther,
                   q.Url,
                   q.Departure.Name,
                   q.get_accepted_display(),
                   q.Points,
                   q.Comment,
                   q.get_date_created(),
                   q.get_date_updated()
                   ]
            try:
                row.append(q.Type)
            except AttributeError:
                pass
            self.lst.append(row)


# Класс для записи в Excel-файл план-факта
class ExcelWriterPlanFact(DepartmentReportMixin, ExcelWriterBase):
    def create_headers(self, workbook, worksheet):
        cell_format = workbook.add_format(BASE_FORMAT_PARAMS)
        
        # Запись верхних заголовков
        for cell_range, title in self.top_headers:
            worksheet.merge_range(cell_range, title, cell_format)
        
        # Установка высоты первой строки
        worksheet.set_row(0, 50)
        
        # Запись второго уровня заголовков
        row_num = 1
        col_start = 1
        col_finish = 17
        sub_headers = ['План', 'Факт', '% Выпол.']

        # Записывает подзаголовки для каждого блока.
        for cell_value in sub_headers:
            for col_num in range(col_start, col_finish, 3):
                worksheet.write(row_num, col_num, cell_value, cell_format)
            col_start += 1
            col_finish += 1
        
    # Формирование строк для записи в файл
    def get_rows(self):
        if self.request.user.is_authenticated:
            for institute in self.queryset:
                self.lst.append([institute.Name])
                deps = Departure.objects.filter(Institute=institute.id)
                for dep in deps:
                    row = [dep.Name]
                    res = self.get_departure_plan_fact(departure=dep, year=self.year)
                    for _, values in res['total'].items():
                        row.extend(list(values.values())[:-1])
                    self.lst.append(row)
 
        
# Класс для экспорта Конференций
class DownloadConferenceExcelView(View):
    def get(self, request, *args, **kwargs):
        # Получаем все записи из модели Conference
        conferences_queryset = Conference.objects.all()
        
        # Если записей нет, возвращаем сообщение
        if not conferences_queryset.exists():
            return HttpResponse("Нет данных для экспорта.")
        
        # Названия столбцов
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
        
        width_colunms = [
            ('A:A', 40),  # Название конференции
            ('B:D', 10),  # Страна, Город, Месяц
            ('E:E', 16),  # Статус
            ('F:F', 13),  # Общее число участников
            ('G:I', 20),  # Кол-во представителей от университета, Ссылка, Email
            ('J:L', 13),  # Студенческая, Организатор университет, Общее число студентов
            ('M:M', 16),  # Кол-во студентов из университета
            ('N:O', 20),  # Список приглашений, Время создания записи
        ]
        
        # Для генерации Excel-файл создаем экземпляр вспомогательного класса
        ew = ExcelWriterConference(request, conferences_queryset, header_columns=header_columns, width_colunms=width_colunms)
        
        # Подготавливаем HTTP-ответ для скачивания файла и генерируем excel-файл
        response = HttpResponse(ew.generate_excel(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-conferences.xlsx"
        
        return response


# Класс для экспорта публикаций (ВАК, тезисы, монографии)
class DownloadPublicationExcelView(View):
    def get(self, request, *args, **kwargs):
        
        model = self.kwargs['model']
        add_columns = False
        
        # Получаем все записи из модели
        if model == 'vak':
            queryset = VAK.objects.all().order_by('-pk')
        elif model == 'thesis':
            queryset = Thesis.objects.all().order_by('-pk')
            add_columns = True
        elif model == 'monograph':
            queryset = Monograph.objects.all().order_by('-pk')
        
        # Если записей нет, возвращаем сообщение
        if not queryset.exists():
            return HttpResponse("Нет данных для экспорта.")
        # Названия столбцов
        header_columns = [
            '№',
            'Название публикации',
            'Название журнала/конференции/isbn',
            'Год',
            'Страницы',
            'Авторы c отчетной кафедры',
            'Авторы с других кафедр',
            'Ссылка',
            'Кафедра',
            'Принято',
            'Кол-во баллов',
            'Комментарий',
            'Дата внесения',
            'Дата последенего изменения',
        ]
        
        if add_columns:
            header_columns.append('Тип конференции')
        
        width_columns = [
            ('A:A', 5),  # №
            ('B:B', 80),  # Название публикации
            ('C:C', 50),  # Название журнала
            ('D:E', 5),  # Год, страницы
            ('F:H', 30),  # Авторы, Ссылка
            ('I:I', 80),  # Кафедра
            ('J:K', 10),  # Принято, кол-во баллов
            ('L:L', 30),  # Комментарий
        ]
        
        # Для генерации Excel-файл создаем экземпляр вспомогательного класса
        ew = ExcelWriterPublication(request, queryset, header_columns=header_columns, width_colunms=width_columns)
        
        # Подготавливаем HTTP-ответ для скачивания файла и генерируем excel-файл
        response = HttpResponse(ew.generate_excel(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response[
            "Content-Disposition"] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-{model}.xlsx"
        return response


# Класс для экспорта план-факта Университета
class DownloadPlanFactAllExcelView(View):
    def get_query_set(self):
        return Institute.objects.all()
      
    def get(self, request, *args, **kwargs):

        queryset = self.get_query_set()
        year = self.kwargs['year']

        # Определение заголовков верхнего уровня
        top_headers = [
            ('A1:A2', 'Структурное подразделение'),
            ('B1:D1', 'Публикации ВАК, шт.'),
            ('E1:G1', 'Тезисы докладов на международных конференциях, шт.'),
            ('H1:J1', 'Тезисы докладов на национальных конференциях, шт.'),
            ('K1:M1', 'Монографии'),
            ('N1:P1', 'Доход, руб.'),
            ('Q1:S1', 'РИД/Патент'),
        ]

        # Определение заголовков второго уровня
        sub_headers = ['План', 'Факт', '% Выпол.']

        width_columns = [
            ('A:A', 80),
            ('N:O', 15),
        ]

        # Для генерации Excel-файл создаем экземпляр вспомогательного класса
        ew = ExcelWriterPlanFact(request, queryset, top_headers=top_headers, sub_headers=sub_headers,
                                   width_colunms=width_columns, year=year, offset=2)

        # Подготавливаем HTTP-ответ для скачивания файла и генерируем excel-файл
        response = HttpResponse(ew.generate_excel(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-plan_fact.xlsx"

        return response
        

# Класс для экспорта план-факта Института
class DownloadPlanFactInstituteExcelView(DownloadPlanFactAllExcelView):
    def get_query_set(self):
        institute_id = self.kwargs['institute_id']
        return Institute.objects.filter(id=institute_id)
