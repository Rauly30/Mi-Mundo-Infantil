"""
URL configuration for escuela project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from panel_profesor.views import panel_profesor
from panel_administrador.views import panel_administrador
from panel_director.views import panel_director

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista home
    path('profesor/', panel_profesor, name='panel_profesor'),
    path('administrador/', panel_administrador, name='panel_administrador'),
    path('director/', panel_director, name='panel_director'),
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticación
]