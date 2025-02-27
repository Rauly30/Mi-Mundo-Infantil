from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password
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
            elif action == 'eliminar':
                # Eliminar un estudiante
                estudiante_id = request.POST.get('id')
                estudiante = get_object_or_404(Estudiante, id=estudiante_id)
                estudiante.delete()

        elif model_type == 'aula':
            if action == 'crear':
                # Crear una nueva aula
                nombre = request.POST.get('nombre')
                nivel = request.POST.get('nivel')
                capacidad = request.POST.get('capacidad')
                profesor_id = request.POST.get('profesor')
                profesor = Profesor.objects.get(id=profesor_id) if profesor_id else None
                Aula.objects.create(nombre=nombre, nivel=nivel, capacidad=capacidad, profesor=profesor)
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
            elif action == 'eliminar':
                # Eliminar un aula
                aula_id = request.POST.get('id')
                aula = get_object_or_404(Aula, id=aula_id)
                aula.delete()

        elif model_type == 'profesor':
            if action == 'crear':
                # Crear un nuevo profesor
                nombre = request.POST.get('nombre')
                especialidad = request.POST.get('especialidad')
                email = request.POST.get('email')
                password = request.POST.get('password')
                Profesor.objects.create(nombre=nombre, especialidad=especialidad, email=email, password=password)
            elif action == 'editar':
                # Editar un profesor existente
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                profesor.nombre = request.POST.get('nombre')
                profesor.especialidad = request.POST.get('especialidad')
                profesor.email = request.POST.get('email')
                profesor.password = request.POST.get('password')
                profesor.save()
            elif action == 'eliminar':
                # Eliminar un profesor
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                profesor.delete()

        elif model_type == 'administrador':
            if action == 'crear':
                # Crear un nuevo administrador
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
                password = request.POST.get('password')
                Administrador.objects.create(nombre=nombre, email=email, password=password)
            elif action == 'editar':
                # Editar un administrador existente
                administrador_id = request.POST.get('id')
                administrador = get_object_or_404(Administrador, id=administrador_id)
                administrador.nombre = request.POST.get('nombre')
                administrador.email = request.POST.get('email')
                administrador.password = request.POST.get('password')
                administrador.save()
            elif action == 'eliminar':
                # Eliminar un administrador
                administrador_id = request.POST.get('id')
                administrador = get_object_or_404(Administrador, id=administrador_id)
                administrador.delete()

        # Redirigir para evitar reenvíos del formulario
        return redirect('panel_administrador')

    # Renderizar el template con los datos
    context = {
        'estudiantes': estudiantes,
        'aulas': aulas,
        'profesores': profesores,
        'administradores': administradores,
    }
    return render(request, 'panel-administrador.html', context)

def panel_director(request):
    return render(request, 'panel-director.html')

def panel_profesor(request):
    return render(request, 'panel-profesor.html')

# API Views
@require_http_methods(["GET", "POST"])
def estudiantes_api(request):
    if request.method == "GET":
        estudiantes = Estudiante.objects.all()
        data = [{
            'id': e.id,
            'nombre': e.nombre,
            'edad': e.edad,
            'nivel': e.nivel,
            'aula': e.aula.nombre if e.aula else None
        } for e in estudiantes]
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        estudiante = Estudiante.objects.create(
            nombre=data['nombre'],
            edad=data['edad'],
            nivel=data['nivel'],
            aula_id=data['aula'] if data['aula'] else None
        )
        return JsonResponse({
            'id': estudiante.id,
            'nombre': estudiante.nombre,
            'edad': estudiante.edad,
            'nivel': estudiante.nivel,
            'aula': estudiante.aula.nombre if estudiante.aula else None
        }, status=201)

@require_http_methods(["GET", "PUT", "DELETE"])
def estudiante_detail_api(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    
    if request.method == "GET":
        data = {
            'id': estudiante.id,
            'nombre': estudiante.nombre,
            'edad': estudiante.edad,
            'nivel': estudiante.nivel,
            'aula': estudiante.aula.nombre if estudiante.aula else None
        }
        return JsonResponse(data)
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        estudiante.nombre = data['nombre']
        estudiante.edad = data['edad']
        estudiante.nivel = data['nivel']
        estudiante.aula_id = data['aula'] if data['aula'] else None
        estudiante.save()
        return JsonResponse({'status': 'success'})
    
    elif request.method == "DELETE":
        estudiante.delete()
        return JsonResponse({'status': 'success'})

@require_http_methods(["GET"])
def aulas_api(request):
    aulas = Aula.objects.all()
    data = [{
        'id': a.id,
        'nombre': a.nombre,
        'nivel': a.nivel,
        'capacidad': a.capacidad
    } for a in aulas]
    return JsonResponse(data, safe=False)

def logout_view(request):
    request.session.flush()
    return redirect('index')

# Vista para el listado de clases
def clases_view(request):
    clases = Clase.objects.all()
    return render(request, 'clases.html', {'clases': clases})

# Vista para el listado de evaluaciones
def evaluaciones_view(request):
    evaluaciones = Evaluacion.objects.all()
    return render(request, 'evaluaciones.html', {'evaluaciones': evaluaciones})

# Vista para el listado de eventos
def eventos_view(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})

# Vista para el listado de profesores
def profesores_view(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores.html', {'profesores': profesores})

# Vista para ver detalles de una clase
def view_class_details(request, clase_id):
    clase = Clase.objects.get(id=clase_id)
    return render(request, 'class_details.html', {'clase': clase})

# Vista para ver el plan de evaluación de una clase
def view_evaluation_plan(request, evaluacion_id):
    evaluacion = Evaluacion.objects.get(id=evaluacion_id)
    return render(request, 'evaluation_plan.html', {'evaluacion': evaluacion})

# Vista para añadir un comentario a una evaluación
def add_comment_to_evaluation(request, evaluacion_id):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        evaluacion = Evaluacion.objects.get(id=evaluacion_id)
        Comentario.objects.create(texto=texto, evaluacion=evaluacion)
        return redirect('view_evaluation_plan', evaluacion_id=evaluacion_id)
    return render(request, 'add_comment.html')

# Vista para añadir un evento
def add_event(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        Evento.objects.create(fecha=fecha, nombre=nombre, descripcion=descripcion)
        return redirect('eventos')
    return render(request, 'add_event.html')

# Vista para editar un evento
def edit_event(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    if request.method == 'POST':
        evento.fecha = request.POST.get('fecha')
        evento.nombre = request.POST.get('nombre')
        evento.descripcion = request.POST.get('descripcion')
        evento.save()
        return redirect('eventos')
    return render(request, 'edit_event.html', {'evento': evento})

# Vista para eliminar un evento
def delete_event(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.delete()
    return redirect('eventos')

# Vista para ver detalles de un profesor
def view_teacher_details(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)
    return render(request, 'teacher_details.html', {'profesor': profesor})

# Vista para añadir un comentario a un profesor
def add_comment_to_teacher(request, profesor_id):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        profesor = Profesor.objects.get(id=profesor_id)
        Comentario.objects.create(texto=texto, profesor=profesor)
        return redirect('view_teacher_details', profesor_id=profesor_id)
    return render(request, 'add_comment.html')