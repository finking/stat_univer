from django.shortcuts import render, redirect
from .models import Institute, Conference, Employee, FAQ
from .forms import ConferenceForm, InstituteForm, HistoryForm


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
