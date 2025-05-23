"""stat_univer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, initial_feature='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), initial_feature='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from django.conf import settings
from .settings import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]

# DEBUG, MEDIA_URL, MEDIA_ROOT из файла settings
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)