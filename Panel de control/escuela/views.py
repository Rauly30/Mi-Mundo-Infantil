# escuela/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_superuser:
        return redirect('panel_administrador')
    elif request.user.groups.filter(name='Profesores').exists():
        return redirect('panel_profesor')
    elif request.user.groups.filter(name='Directores').exists():
        return redirect('panel_director')
    else:
        return HttpResponse("No tienes permisos para acceder a ningún panel.")