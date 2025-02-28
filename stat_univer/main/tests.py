from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, resolve
from .views import *
from .models import Conference, Departure, Employee
from .forms import ConferenceForm
from model_bakery import baker


# ******* Начало проверки Views *********
class TestLoginUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_user_template(self):
        # Проверяем, что используется правильный шаблон
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        
        
class TestPassChangeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_pass_change_template(self):
        # Проверяем, что используется правильный шаблон
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/password_change.html')
        
        
class TestPassChangeDoneView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_pass_change_done_template(self):
        # Проверяем, что используется правильный шаблон
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/password_change_done.html')
        

class DashboardViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = DashboardView.as_view()

    def test_get_context_data(self):
        # Создаем запрос с параметром year=2023
        request = self.factory.get(reverse('dashboard', kwargs={'year': 2023}))
        response = self.view(request, year=2023)
        context = response.context_data

        # Проверяем наличие ключей в контексте
        self.assertIn('year', context)
        self.assertEqual(context['year'], 2023)
        self.assertIn('title', context)
        self.assertEqual(context['title'], "План-факт по науке за 2023 год")
        self.assertIn('feature', context)
        self.assertEqual(context['feature'], 'Количество публикаций в журналах ВАК')
        self.assertIn('objects', context)
        
        
class TestViewConference(TestCase):
    def setUp(self):
        self.client = Client()
        self.conference_url = reverse('conference')
        self.conference = baker.make(Conference, Name='Тестовая конференция для Views')
    
    def test_request_GET(self):
        response = self.client.get(self.conference_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/conference.html')
        self.assertContains(response, "Name")
        self.assertContains(response, "Total")
    
    def test_request_POST(self):
        conference_count = Conference.objects.count()
        response = self.client.post(self.conference_url, {
            'Name': 'Тестовая конференция для POST',
            'Country': 'RU',
            'City': 'Волгоград',
            'Status': 'М',  # Кириллица!
            'Month': 'Mar',
            'Organizer': False,
            'Student': True,
            'Total': 100,
            'Delegate': 10
        })
        
        self.assertEquals(response.status_code, 302)
        self.assertEqual(Conference.objects.count(), conference_count + 1)
        self.assertRedirects(response, "/conference")


class TestViewIndex(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')


class TestViewInstitute(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('institute'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/institute.html')


class TestViewHistory(TestCase):
    def setUp(self):
        self.client = Client()
        self.conference_url = reverse('conference')
        self.email = "test@ya.ru"
        self.conference = baker.make(Conference, Name='Тестовая конференция для History', Email=self.email)
    
    def test_request_GET(self):
        response = self.client.get(reverse('history'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/history.html')
        self.assertContains(response, "email")


class TestViewFAQ(TestCase):
    def test_request_GET(self):
        response = self.client.get(reverse('faq'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/faq.html')
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
            Director=self.director,
            DeputeScience=self.depute
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

