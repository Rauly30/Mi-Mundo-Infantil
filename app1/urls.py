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
    path('logout/', views.logout_view, name='logout'),
    
    # API URLs
    path('api/estudiantes/', views.estudiantes_api, name='estudiantes_api'),
    path('api/estudiantes/<int:id>/', views.estudiante_detail_api, name='estudiante_detail_api'),
    path('api/aulas/', views.aulas_api, name='aulas_api'),

    # Vistas adicionales
    path('clases/', views.clases_view, name='clases'),
    path('evaluaciones/', views.evaluaciones_view, name='evaluaciones'),
    path('eventos/', views.eventos_view, name='eventos'),
    path('profesores/', views.profesores_view, name='profesores'),
    path('clase/<int:clase_id>/', views.view_class_details, name='view_class_details'),
    path('evaluacion/<int:evaluacion_id>/', views.view_evaluation_plan, name='view_evaluation_plan'),
    path('evaluacion/<int:evaluacion_id>/comentario/', views.add_comment_to_evaluation, name='add_comment_to_evaluation'),
    path('evento/nuevo/', views.add_event, name='add_event'),
    path('evento/<int:evento_id>/editar/', views.edit_event, name='edit_event'),
    path('evento/<int:evento_id>/eliminar/', views.delete_event, name='delete_event'),
    path('profesor/<int:profesor_id>/', views.view_teacher_details, name='view_teacher_details'),
    path('profesor/<int:profesor_id>/comentario/', views.add_comment_to_teacher, name='add_comment_to_teacher'),
]