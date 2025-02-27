from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import json
from .models import Administrador, Profesor, Director, Estudiante, Aula, Clase, Evaluacion, Evento, Comentario

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
    return render(request, 'panel-administrador.html')

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