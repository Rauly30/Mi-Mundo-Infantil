from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import json
from .models import Administrador, Profesor, Director, Estudiante, Aula, Clase, Evaluacion, Evento, Comentario
from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    return render(request, 'index.html')

# Vistas de login para los paneles
def administrador_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Administrador.objects.get(email=email)
            if check_password(password, admin.password):
                request.session['admin_id'] = admin.id
                return redirect('panel_administrador')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'adimistrador_login.html')

def director_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            director = Director.objects.get(email=email)
            if check_password(password, director.password):
                request.session['admin_id'] = director.id
                return redirect('panel_director')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Director.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'director_login.html')

def profesor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            profesor = Profesor.objects.get(email=email)
            if check_password(password, profesor.password):
                request.session['admin_id'] = profesor.id
                return redirect('panel_profesor')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Profesor.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'profesor_login.html')

# Vista de control de paneles
def panel_administrador(request):
    # Obtener el ID del administrador de la sesión
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('administrador_login')
    
    # Obtener el objeto Administrador
    try:
        administrador = Administrador.objects.get(id=admin_id)
    except Administrador.DoesNotExist:
        messages.error(request, 'Administrador no encontrado. Por favor, inicie sesión nuevamente.')
        return redirect('administrador_login')
    
    # Obtener todos los datos para mostrar en el template
    estudiantes = Estudiante.objects.all()
    aulas = Aula.objects.all()
    profesores = Profesor.objects.all()
    administradores = Administrador.objects.all()

    # Manejar las acciones CRUD
    if request.method == 'POST':
        action = request.POST.get('action')  # Acción: crear, editar, eliminar
        model_type = request.POST.get('model_type')  # Tipo de modelo: estudiante, aula, profesor, administrador

        if model_type == 'estudiante':
            if action == 'crear':
                # Crear un nuevo estudiante
                nombre = request.POST.get('nombre')
                edad = request.POST.get('edad')
                nivel = request.POST.get('nivel')
                aula_id = request.POST.get('aula')
                aula = Aula.objects.get(id=aula_id) if aula_id else None
                Estudiante.objects.create(nombre=nombre, edad=edad, nivel=nivel, aula=aula)
                messages.success(request, 'Estudiante agregado exitosamente.')
            elif action == 'editar':
                # Editar un estudiante existente
                estudiante_id = request.POST.get('id')
                estudiante = get_object_or_404(Estudiante, id=estudiante_id)
                estudiante.nombre = request.POST.get('nombre')
                estudiante.edad = request.POST.get('edad')
                estudiante.nivel = request.POST.get('nivel')
                aula_id = request.POST.get('aula')
                estudiante.aula = Aula.objects.get(id=aula_id) if aula_id else None
                estudiante.save()
                messages.success(request, 'Estudiante editado exitosamente.')
            elif action == 'eliminar':
                # Eliminar un estudiante
                estudiante_id = request.POST.get('id')
                estudiante = get_object_or_404(Estudiante, id=estudiante_id)
                estudiante.delete()
                messages.success(request, 'Estudiante eliminado exitosamente.')

        elif model_type == 'aula':
            if action == 'crear':
                # Crear una nueva aula
                nombre = request.POST.get('nombre')
                nivel = request.POST.get('nivel')
                capacidad = request.POST.get('capacidad')
                profesor_id = request.POST.get('profesor')
                profesor = Profesor.objects.get(id=profesor_id) if profesor_id else None
                Aula.objects.create(nombre=nombre, nivel=nivel, capacidad=capacidad, profesor=profesor)
                messages.success(request, 'Aula agregada exitosamente.')
            elif action == 'editar':
                # Editar un aula existente
                aula_id = request.POST.get('id')
                aula = get_object_or_404(Aula, id=aula_id)
                aula.nombre = request.POST.get('nombre')
                aula.nivel = request.POST.get('nivel')
                aula.capacidad = request.POST.get('capacidad')
                profesor_id = request.POST.get('profesor')
                aula.profesor = Profesor.objects.get(id=profesor_id) if profesor_id else None
                aula.save()
                messages.success(request, 'Aula editada exitosamente.')
            elif action == 'eliminar':
                # Eliminar un aula
                aula_id = request.POST.get('id')
                aula = get_object_or_404(Aula, id=aula_id)
                aula.delete()
                messages.success(request, 'Aula eliminada exitosamente.')

        elif model_type == 'profesor':
            if action == 'crear':
                # Crear un nuevo profesor
                nombre = request.POST.get('nombre')
                especialidad = request.POST.get('especialidad')
                email = request.POST.get('email')
                password = make_password(request.POST.get('password'))
                Profesor.objects.create(nombre=nombre, especialidad=especialidad, email=email, password=password)
                messages.success(request, 'Profesor agregado exitosamente.')
            elif action == 'editar':
                # Editar un profesor existente
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                profesor.nombre = request.POST.get('nombre')
                profesor.especialidad = request.POST.get('especialidad')
                profesor.email = request.POST.get('email')
                if request.POST.get('password'):
                    profesor.password = make_password(request.POST.get('password'))
                profesor.save()
                messages.success(request, 'Profesor editado exitosamente.')
            elif action == 'eliminar':
                # Eliminar un profesor
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                profesor.delete()
                messages.success(request, 'Profesor eliminado exitosamente.')

        elif model_type == 'administrador':
            if action == 'crear':
                # Crear un nuevo administrador
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
                password = make_password(request.POST.get('password'))
                Administrador.objects.create(nombre=nombre, email=email, password=password)
                messages.success(request, 'Administrador agregado exitosamente.')
            elif action == 'editar':
                # Editar un administrador existente
                administrador_id = request.POST.get('id')
                administrador = get_object_or_404(Administrador, id=administrador_id)
                administrador.nombre = request.POST.get('nombre')
                administrador.email = request.POST.get('email')
                if request.POST.get('password'):
                    administrador.password = make_password(request.POST.get('password'))
                administrador.save()
                messages.success(request, 'Administrador editado exitosamente.')
            elif action == 'eliminar':
                # Eliminar un administrador
                administrador_id = request.POST.get('id')
                administrador = get_object_or_404(Administrador, id=administrador_id)
                administrador.delete()
                messages.success(request, 'Administrador eliminado exitosamente.')

        # Redirigir para evitar reenvíos del formulario
        return redirect('panel_administrador')

    # Renderizar el template con los datos
    context = {
        'administrador': administrador,
        'estudiantes': estudiantes,
        'aulas': aulas,
        'profesores': profesores,
        'administradores': administradores,
    }
    return render(request, 'panel-administrador.html', context)


from django.shortcuts import render
from .models import Profesor, Evento, Evaluacion, Clase, Comentario

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profesor, Evento, Evaluacion, Clase, Comentario

def panel_director(request):
    # Obtener todos los datos necesarios
    profesores = Profesor.objects.all()
    eventos = Evento.objects.all()
    evaluaciones = Evaluacion.objects.all()
    clases = Clase.objects.all()
    comentarios = Comentario.objects.all()

    # Manejar solicitudes POST
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "registrar_clase":
            # Obtener los datos del formulario
            grado = request.POST.get("grado")
            profesor_id = request.POST.get("profesor")
            numero_estudiantes = request.POST.get("numero_estudiantes")

            # Validar y guardar la nueva clase
            if grado and profesor_id and numero_estudiantes:
                profesor = Profesor.objects.get(id=profesor_id)
                nueva_clase = Clase(
                    grado=grado,
                    profesor=profesor,
                    numero_estudiantes=numero_estudiantes
                )
                nueva_clase.save()
                messages.success(request, "Clase registrada correctamente.")
            else:
                messages.error(request, "Todos los campos son obligatorios.")

            return redirect("panel_director")

        elif action == "editar_clase":
            # Código existente para editar una clase
            pass

    # Pasar los datos al template
    context = {
        'profesores': profesores,
        'eventos': eventos,
        'evaluaciones': evaluaciones,
        'clases': clases,
        'comentarios': comentarios,
    }
    return render(request, 'panel-director.html', context)

def panel_profesor(request):
    return render(request, 'panel-profesor.html')


def logout_view(request):
    request.session.flush()
    return redirect('index')