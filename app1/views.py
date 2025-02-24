from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Administrador, Profesor, Director
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')
# Create your views here.

#vista de logins para los paneles

def administrador_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Administrador.objects.get(email=email)

            # Verificar la contraseña
            if check_password(password, admin.password):  # Comprobar si la contraseña es correcta
                request.session['admin_id'] = admin.id  # Guardar el ID del admin en la sesión
                return redirect('panel_administrador')  # Redirigir al panel de control de usuarios
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')

        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos .')

    return render(request, 'adimistrador_login.html')

def director_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            director = Director.objects.get(email=email)

            # Verificar la contraseña
            if check_password(password, director.password):  # Comprobar si la contraseña es correcta
                request.session['admin_id'] = director.id  # Guardar el ID del admin en la sesión
                return redirect('panel_director')  # Redirigir al panel de control de usuarios
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')

        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos .')

    return render(request, 'director_login.html')

def profesor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            profesor = Profesor.objects.get(email=email)

            # Verificar la contraseña
            if check_password(password, profesor.password):  # Comprobar si la contraseña es correcta
                request.session['admin_id'] = profesor.id  # Guardar el ID del admin en la sesión
                return redirect('panel_profesor')  # Redirigir al panel de control de usuarios
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')

        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos .')

    return render(request, 'profesor_login.html')

#Vista de control de paneles
def panel_administrador(request):
    return render(request, 'panel-administrador.html')

def panel_director(request):
    return render(request, 'panel-director.html')

def panel_profesor(request):
    return render(request, 'panel-profesor.html')