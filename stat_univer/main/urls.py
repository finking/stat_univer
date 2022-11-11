from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bd/', views.vvod, name="vvod"),
    path('institute', views.institute, name='institute'),
    path('department', views.department, name='department'),
    path('lecturer', views.lecturer, name='lecturer'),
    path('conference', views.conference, name='conference'),
    path('history', views.history, name='history'),
    path('faq', views.faq, name='faq'),
    path('success', views.success, name='success'),
    path('export', views.export, name='export'),
    path('export_pf_all', views.export_pf_all, name='export_pf_all'),
    path('export_pf/<int:institute_id>', views.export_pf, name='export_pf'),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
    path('vak', views.vak, name='vak'),
    path('edit/<int:publication_id>/<str:type>', views.edit, name='edit'),
    path('main', views.main, name='main'),
    path('thesis', views.thesis, name='thesis'),
    path('monograph', views.monograph, name='monograph'),
    path('report/<int:institute_id>', views.report, name='report'),
    path('catalogue/<int:department_id>/<str:type>', views.catalogue, name='catalogue'),
]
