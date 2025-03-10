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
    path('api/estudiantes/', views.estudiantes_api, name='estudiantes_api'),
    path('api/estudiantes/<int:id>/', views.estudiante_detail_api, name='estudiante_detail_api'),
    path('api/aulas/', views.aulas_api, name='aulas_api'),
    path('api/aulas/<int:aula_id>/estudiantes/', views.estudiantes_por_aula_api, name='estudiantes_por_aula_api'),
    path('logout/', views.logout_view, name='logout'),
    path('evaluaciones/', views.evaluaciones_view, name='evaluaciones_view'),
    path('eventos/', views.eventos_view, name='eventos_view'),
    path('profesores/', views.profesores_view, name='profesores_view'),
]