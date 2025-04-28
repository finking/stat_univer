from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from .sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    # Авторизация
    path('login_user', views.LoginUser.as_view(), name='login'),
    path('logout_user', LogoutView.as_view(), name='logout'),
    path('change-password/', views.PassChangeView.as_view(), name='change-password'),
    path('change-password/done/', views.PassChangeDoneView.as_view(), name='password_change_done'),
    
    # Визуализация
    path('dashboard/<int:year>', views.DashboardView.as_view(), name='dashboard'),
    
    # Отображение общей информации
    path('', views.Index.as_view(), name='index'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('institute', views.InstituteList.as_view(), name='institute'),
    path('faq', views.FaqView.as_view(), name='faq'),
    
    # Форма внесения конференции и история внесения
    path('conference', views.ConferenceView.as_view(), name='conference'),
    path('history', views.HistoryView.as_view(), name='history'),

    # Новые данные по публикациям, доходу и РИД
    path('vak', views.VakCreateView.as_view(), name='vak_create'),
    path('thesis', views.ThesisCreateView.as_view(), name='thesis_create'),
    path('monograph', views.MonographCreateView.as_view(), name='monograph_create'),
    path('income', views.IncomeCreateView.as_view(), name='income_create'),
    path('rid', views.RidCreateView.as_view(), name='rid_create'),
    
    # Изменение данных по публикациям, доходу и РИД
    path('vak/update/<int:pk>', views.VakEditView.as_view(), name='vak_update'),
    path('thesis/update/<int:pk>', views.ThesisEditView.as_view(), name='thesis_update'),
    path('monograph/update/<int:pk>', views.MonographEditView.as_view(), name='monograph_update'),
    path('income/update/<int:pk>', views.IncomeEditView.as_view(), name='income_update'),
    path('rid/update/<int:pk>', views.RidEditView.as_view(), name='rid_update'),

    # Отчеты по вузу и институтам для отображения на сайте
    path('institutes/year/<int:year>/', views.InstituteReportListView.as_view(), name='main'),
    path('report/<int:institute_id>/<int:year>', views.DepartmentReportListView.as_view(), name='report'),
    
    # Списки по публикациям всего университета
    path('vakList', views.VakListView.as_view(), name='vakList'),
    path('thesisList', views.ThesisListView.as_view(), name='thesisList'),
    path('monographList', views.MonographListView.as_view(), name='monographList'),
    
    # Списки по публикациям, доходу и РИД для каждой кафедры
    path('vakListDeparture/<int:department_id>/<int:year>', views.VakListDepartureView.as_view(),
         name='vak_list_departure'),
    path('thesisListDeparture/<int:department_id>/<int:year>', views.ThesisListDepartureView.as_view(),
         name='thesis_list_departure'),
    path('monographListDeparture/<int:department_id>/<int:year>', views.MonographListDepartureView.as_view(),
         name='monograph_list_departure'),
    path('incomeListDeparture/<int:department_id>/<int:year>', views.IncomeListDepartureView.as_view(),
         name='income_list_departure'),
    path('ridListDeparture/<int:department_id>/<int:year>', views.RidListDepartureView.as_view(),
         name='rid_list_departure'),
    
    # Экспорт данных
    path('export_conference', views.DownloadConferenceExcelView.as_view(), name='export'),
    path('export_publications/<str:model>', views.DownloadPublicationExcelView.as_view(), name='export_publications'),
    path('export_pf_all/<int:year>', views.DownloadPlanFactAllExcelView.as_view(), name='export_pf_all'),
    path('export_pf/<int:institute_id>/<int:year>', views.DownloadPlanFactInstituteExcelView.as_view(),
         name='export_pf'),
    
    # Карта сайта
    path(
            "sitemap.xml",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
]
