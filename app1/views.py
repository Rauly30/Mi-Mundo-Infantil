from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def index(request):
    return render(request, 'index.html')
# Create your views here.



def is_administrador(user):
    return user.is_superuser

@login_required
@user_passes_test(is_administrador)
def panel_administrador(request):
    return render(request, 'panel-administrador.html')

def is_director(user):
    return user.groups.filter(name='Directores').exists()

@login_required
@user_passes_test(is_director)
def panel_director(request):
    return render(request, 'panel-director.html')

def is_profesor(user):
    return user.groups.filter(name='Profesores').exists()

@login_required
@user_passes_test(is_profesor)
def panel_profesor(request):
    return render(request, 'panel-profesor.html')