from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profesor/',views.panel_profesor, name='panel_profesor'),
    path('administrador/', views.panel_administrador, name='panel_administrador'),
    path('director/', views.panel_director, name='panel_director'),

]