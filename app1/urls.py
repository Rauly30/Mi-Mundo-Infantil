from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('panel_profesorr/',views.panel_profesor, name='panel_profesor'),
    path('panel_administrador/', views.panel_administrador, name='panel_administrador'),
    path('panel_director/', views.panel_director, name='panel_director'),
    path('administrador_login/', views.administrador_login, name='administrador_login'),
    path('profesor_login/', views.profesor_login, name='profesor_login'),

]