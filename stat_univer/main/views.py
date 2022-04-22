from django.shortcuts import render, redirect
from .models import Institute, Conference, Employee, FAQ
from .forms import ConferenceForm, InstituteForm, HistoryForm
from django.http import HttpResponse
from datetime import datetime
from xlsxwriter.workbook import Workbook
import io
from .utils import dict_from_tuple, binary, MONTH, STATUS, COUNTRY


def index(request):
    return render(request, 'main/index.html')


def vvod(request):
    return render(request, 'main/vvod.html')


def success(request):
    return render(request, 'main/success.html')


def institute(request):
    dictInstitute = {}
    institutes = Institute.objects.order_by('-id')
    if institutes:
        for i in institutes:
            NameInstitute = i.Name
            Director = Employee.objects.filter(Name=i.IdDirector)
            dictInstitute.setdefault(NameInstitute, Director)
        print(dictInstitute)
    error = ''
    if request.method == 'POST':
        form = InstituteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vvod')
        else:
            error = 'Произошла ошибка. Данные Института не отправлены.'
            print(form.cleaned_data)

    else:
        form = InstituteForm()

    return render(request, 'main/institute.html', {'title': 'Институты ГУУ',
                                                   'institutes': institutes,
                                                   'form': form,
                                                   'error': error})


def department(request):
    return render(request, 'main/department.html')


def lecturer(request):
    return render(request, 'main/lecturer.html')


def conference(request):
    error = ''
    if request.method == 'POST':
        form = ConferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            error = 'Произошла ошибка. Данные конференции не отправлены.'
            # print(form.cleaned_data)
    else:
        form = ConferenceForm()

    context = {'form': form,
               'error': error}
    return render(request, 'main/conference.html', context)


def history(request):
    message = ''
    conferences_history = None
    qty_history = 0
    method = 1
    error = ''
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
            except Exception as e:
                print(f"Ошибка: {e}")

        else:
            # error = 'Произошла ошибка. Данные конференции не отправлены.'
            # print(form.cleaned_data)
            pass
    else:
        form = HistoryForm()

    context = {'conferences_history': conferences_history,
               'qty_history': qty_history,
               'message': message,
               'method': method,
               'form': form}
    return render(request, 'main/history.html', context)


def faq(request):
    faqs = FAQ.objects.order_by('id')
    return render(request, 'main/faq.html', {'faqs': faqs})


def export(request):
    conferences_queryset = Conference.objects.all()

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
    for conference in conferences_queryset:
        row_num += 1

        # Поиск необходимых значеий в соответствующих словарях
        month = dict_month[conference.Month]
        country = dict_country[conference.Country]
        status = dict_status[conference.Status]
        student = binary(conference.Student)  # Студенческая или нет
        organizer = binary(conference.Organizer)  # Организатор ГУУ или нет
        
        timeCreate = conference.TimeCreate.strftime("%d-%m-%Y %H:%M:%S")  # Преобразование времени в строковый формат

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

    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%d-%m-%Y')}-conferences.xlsx"

    output.close()

    return response
