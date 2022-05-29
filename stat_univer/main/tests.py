from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import *
from .models import Conference, Departure
from .forms import ConferenceForm
from model_bakery import baker


# Проверка url адресов.
class TestUrls(TestCase):
    
    def test_url_index(self):
        url = reverse('index')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_url_vvod(self):
        url = reverse('vvod')
        self.assertEquals(resolve(url).func, vvod)
        
    def test_url_institute(self):
        url = reverse('institute')
        self.assertEquals(resolve(url).func, institute)
    
    def test_url_department(self):
        url = reverse('department')
        self.assertEquals(resolve(url).func, department)
    
    def test_url_lecturer(self):
        url = reverse('lecturer')
        self.assertEquals(resolve(url).func, lecturer)

    def test_url_conference(self):
        url = reverse('conference')
        self.assertEquals(resolve(url).func, conference)

    def test_url_history(self):
        url = reverse('history')
        self.assertEquals(resolve(url).func, history)

    def test_url_faq(self):
        url = reverse('faq')
        self.assertEquals(resolve(url).func, faq)

    def test_url_success(self):
        url = reverse('success')
        self.assertEquals(resolve(url).func, success)
        
    def test_url_export(self):
        url = reverse('export')
        self.assertEquals(resolve(url).func, export)

    def test_url_login_user(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_user)

    def test_url_logout_user(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_user)

    def test_url_profile(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_url_vak(self):
        url = reverse('vak')
        self.assertEquals(resolve(url).func, vak)

# ******* Начало проверки Views *********
class TestViewConference(TestCase):
    def setUp(self):
        self.client = Client()
        self.conference_url = reverse('conference')
        self.conference = baker.make(Conference, Name='Тестовая конференция для Views')
    
    def test_request_GET(self):
        response = self.client.get(self.conference_url)
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/conference.html')
        self.assertContains(response, "Name")
        self.assertContains(response, "Total")

    def test_request_POST(self):
        conference_count = Conference.objects.count()
        response = self.client.post(self.conference_url, {
            'Name': 'Тестовая конференция для POST',
            'Country': 'RU',
            'City': 'Волгоград',
            'Status': 'М', # Кириллица!
            'Month': 'Mar',
            'Organizer': False,
            'Student': True,
            'Total': 100,
            'Delegate': 10
        })

        self.assertEquals(response.status_code, 302)
        self.assertEqual(Conference.objects.count(), conference_count+1)
        self.assertRedirects(response, "/success")


class TestViewIndex(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/index.html')


class TestViewVvod(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('vvod'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/vvod.html')
        
        
class TestViewSuccess(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('success'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/success.html')
        
        
class TestViewInstitute(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('institute'))
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/institute.html')
        

class TestViewDepartment(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('department'))
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/department.html')
        
        
class TestViewLecture(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('lecturer'))
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/lecturer.html')


class TestViewHistory(TestCase):
    def setUp(self):
        self.client = Client()
        self.conference_url = reverse('conference')
        self.email = "test@ya.ru"
        self.conference = baker.make(Conference, Name='Тестовая конференция для History', Email=self.email)
    
    def test_request_GET(self):
        response = self.client.get(reverse('history'))
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/history.html')
        self.assertContains(response, "email")

    # def test_request_POST(self): # TODO разобраться как проверять подобный post запрос. Когда данные не вносятся в бд, а выбираются!
    #     response = self.client.post(reverse('history'), {'Email': 'test@ya.ru'})
    #     conferences_history = Conference.objects.filter(Email=self.email)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEqual(len(conferences_history), 1)
    #     # self.assertRedirects(response, "/success") # TODO Нужен ли редирект в history?
    

class TestViewFAQ(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('faq'))
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'main/faq.html')
        

class TestViewExport(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('export'))
        # print(response.headers['Content-Disposition'])
        self.assertEquals(response.headers['Content-Type'],
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertEquals(response.headers['Content-Disposition'],
                          f"attachment; "f"filename={datetime.now().strftime('%d-%m-%Y')}-conferences.xlsx")
        self.assertEquals(response.status_code,  200)
# ******* Окончание проверки Views *********

# ******* Начало проверки Forms *********
class TestFormsConference(TestCase):
    def test_conference_form_valid_data(self):
        form = ConferenceForm(data={
            'Name': 'Тестовая конференция Для Form',
            'Country': 'RU',
            'City': 'Волгоград',
            'Status': 'М',  # Кириллица!
            'Month': 'Mar',
            'Organizer': False,
            'Student': True,
            'Total': 100,
            'Delegate': 10

        })
        self.assertTrue(form.is_valid())
        
    def test_conference_form_no_data(self):
        form = ConferenceForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)
        # TODO Должно быть 8 ошибок, т.к. 8 обязательных поля! Name-необязательное, а Organizer и Student -
        #  обязательны по Forms.py??


class TestFormsHistory(TestCase):
    def test_history_form_valid_data(self):
        form = HistoryForm(data={'email': 'test@ya.ru'})
        self.assertTrue(form.is_valid())
    
    def test_history_form_no_valid_data(self):
        form = HistoryForm(data={'email': 'testya.ru'})
        self.assertFalse(form.is_valid())
    
    def test_history_form_no_data(self):
        form = HistoryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        
# TODO Протестировать Forms, которые только в Admin: Institute и FAQ

# ******* Окончание проверки Forms *********

# ******* Начало проверки Models *********
class TestModelsConference(TestCase):
    def setUp(self):
        self.conference = baker.make(Conference, Name='Тестовая конференция для Model')
    
    def test_model_str(self):
        self.assertEqual(str(self.conference), "Тестовая конференция для Model")


class TestModelsIntitute(TestCase):
    def setUp(self):
        self.director = baker.make(Employee)
        self.depute = baker.make(Employee)
        self.institute = Institute.objects.create(
            Name='Институт благородных дел',  # TODO Исправить в models.py описание ошибки
            ShortName='ИБД',
            IdDirector=self.director,
            IdDeputeScience=self.depute
        )

    def test_model_str(self):
        self.assertEqual(str(self.institute), "Институт благородных дел")


class TestModelsEmployee(TestCase):
    def setUp(self):
        self.employee = baker.make(Employee, Name='Иван', MiddleName='Владимирович', Surname='Сидоров')
    
    def test_model_str(self):
        self.assertEqual(str(self.employee), "Сидоров Иван Владимирович")


class TestModelsDeparture(TestCase):
    def setUp(self):
        self.departure = baker.make(Departure, Name='Кафедра тестирования')
    
    def test_model_str(self):
        self.assertEqual(str(self.departure), "Кафедра тестирования")


class TestModelsFaq(TestCase):
    def setUp(self):
        self.faq = baker.make(FAQ, Question='Вопрос первый.')
    
    def test_model_str(self):
        self.assertEqual(str(self.faq), "Вопрос первый.")
        
# ******* Окончание проверки Models *********
