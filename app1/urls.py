from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('administrador/login/', views.administrador_login, name='administrador_login'),
    path('director/login/', views.director_login, name='director_login'),
    path('profesor/login/', views.profesor_login, name='profesor_login'),
    path('panel/administrador/', views.panel_administrador, name='panel_administrador'),
    path('panel/director/', views.panel_director, name='panel_director'),
    path('panel/profesor/', views.panel_profesor, name='panel_profesor'),
    path('logout/', views.logout, name='logout'),
    path('api/aulas/<int:aula_id>/estudiantes/', views.get_estudiantes, name='get_estudiantes'),
]