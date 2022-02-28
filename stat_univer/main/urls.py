from django.urls import path
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
    path('success', views.success, name='success')
]
