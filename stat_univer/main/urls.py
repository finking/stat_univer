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
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
]
