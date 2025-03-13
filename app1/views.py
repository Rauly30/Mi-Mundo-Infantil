from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import json
from .models import Administrador, Profesor, Director, Estudiante, Aula, Evaluacion, Evento, Comentario

def index(request):
    return render(request, 'index.html')

# Vistas de login para los paneles
def administrador_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            administrador = Administrador.objects.get(email=email)
            if check_password(password, administrador.password):
                request.session['administrador_id'] = administrador.id  # Guarda el ID del administrador en la sesión
                return redirect('panel_administrador')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'administrador_login.html')

def director_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            director = Director.objects.get(email=email)
            if check_password(password, director.password):
                request.session['director_id'] = director.id
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
                request.session['profesor_id'] = profesor.id  # Correct session variable
                return redirect('panel_profesor')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Profesor.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'profesor_login.html')

# Vista de control de paneles
def panel_administrador(request):
    # Verificar si el administrador está autenticado
    administrador_id = request.session.get('administrador_id')
    if not administrador_id:
        messages.error(request, 'Por favor, inicie sesión para acceder al panel.')
        return redirect('administrador_login')

    # Obtener el objeto Administrador
    try:
        administrador = Administrador.objects.get(id=administrador_id)
    except Administrador.DoesNotExist:
        messages.error(request, 'Administrador no encontrado. Por favor, inicie sesión nuevamente.')
        return redirect('administrador_login')
    
    # Obtener todos los datos para mostrar en el template
    estudiantes = Estudiante.objects.all()
    aulas = Aula.objects.all()
    profesores = Profesor.objects.all()
    directores = Director.objects.all()
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
        elif model_type == 'director':
            if action == 'crear':
                # Crear un nuevo director
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
                password = make_password(request.POST.get('password'))
                Director.objects.create(nombre=nombre, email=email, password=password)
                messages.success(request, 'Director agregado exitosamente.')
            elif action == 'editar':
                # Editar un director existente
                director_id = request.POST.get('id')
                director = get_object_or_404(Director, id=director_id)
                director.nombre = request.POST.get('nombre')
                director.email = request.POST.get('email')
                if request.POST.get('password'):
                    director.password = make_password(request.POST.get('password'))
                director.save()
                messages.success(request, 'Director editado exitosamente.')
            elif action == 'eliminar':
                # Eliminar un director
                director_id = request.POST.get('id')
                director = get_object_or_404(Director, id=director_id)
                director.delete()
                messages.success(request, 'Director eliminado exitosamente.')

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
        'directores': directores,
        'administradores': administradores,
    }
    return render(request, 'panel-administrador.html', context)

def panel_director(request):

    # Verificar si el administrador está autenticado
    director_id = request.session.get('director_id')
    if not director_id:
        messages.error(request, 'Por favor, inicie sesión para acceder al panel.')
        return redirect('director_login')

    # Obtener el objeto Administrador
    try:
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        messages.error(request, 'Administrador no encontrado. Por favor, inicie sesión nuevamente.')
        return redirect('administrador_login')
    
    aulas = Aula.objects.all()
    evaluaciones = Evaluacion.objects.all()
    eventos = Evento.objects.all()
    profesores = Profesor.objects.all()

    # Obtener todos los comentarios relacionados con evaluaciones
    comentarios_evaluaciones = Comentario.objects.filter(evaluacion__isnull=False)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'agregar_evento':
            fecha = request.POST.get('fecha')
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            Evento.objects.create(fecha=fecha, nombre=nombre, descripcion=descripcion)
            messages.success(request, 'Evento agregado exitosamente.')

        elif action == 'editar_evento':
            evento_id = request.POST.get('id')
            evento = get_object_or_404(Evento, id=evento_id)
            evento.fecha = request.POST.get('fecha')
            evento.nombre = request.POST.get('nombre')
            evento.descripcion = request.POST.get('descripcion')
            evento.save()
            messages.success(request, 'Evento editado exitosamente.')

        elif action == 'eliminar_evento':
            evento_id = request.POST.get('id')
            evento = get_object_or_404(Evento, id=evento_id)
            evento.delete()
            messages.success(request, 'Evento eliminado exitosamente.')

        elif action == 'agregar_evaluacion':
            aula_id = request.POST.get('aula')
            plan = request.POST.get('plan')
            Evaluacion.objects.create(aula_id=aula_id, plan=plan)
            messages.success(request, 'Evaluación agregada exitosamente.')

        elif action == 'editar_evaluacion':
            evaluacion_id = request.POST.get('id')
            evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
            evaluacion.aula_id = request.POST.get('aula')
            evaluacion.plan = request.POST.get('plan')
            evaluacion.save()
            messages.success(request, 'Evaluación editada exitosamente.')

        elif action == 'eliminar_evaluacion':
            evaluacion_id = request.POST.get('id')
            evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
            evaluacion.delete()
            messages.success(request, 'Evaluación eliminada exitosamente.')

        elif action == 'agregar_profesor':
            nombre = request.POST.get('nombre')
            especialidad = request.POST.get('especialidad')
            email = request.POST.get('email')
            password = make_password(request.POST.get('password'))
            Profesor.objects.create(nombre=nombre, especialidad=especialidad, email=email, password=password)
            messages.success(request, 'Profesor agregado exitosamente.')

        elif action == 'editar_profesor':
            profesor_id = request.POST.get('id')
            profesor = get_object_or_404(Profesor, id=profesor_id)
            profesor.nombre = request.POST.get('nombre')
            profesor.especialidad = request.POST.get('especialidad')
            profesor.email = request.POST.get('email')
            if request.POST.get('password'):
                profesor.password = make_password(request.POST.get('password'))
            profesor.save()
            messages.success(request, 'Profesor editado exitosamente.')

        elif action == 'eliminar_profesor':
            profesor_id = request.POST.get('id')
            profesor = get_object_or_404(Profesor, id=profesor_id)
            profesor.delete()
            messages.success(request, 'Profesor eliminado exitosamente.')

        elif action == 'registrar_aula':
            nombre = request.POST.get('nombre')
            nivel = request.POST.get('nivel')
            capacidad = request.POST.get('capacidad')
            profesor_id = request.POST.get('profesor')
            profesor = Profesor.objects.get(id=profesor_id)
            Aula.objects.create(nombre=nombre, nivel=nivel, capacidad=capacidad, profesor=profesor)
            messages.success(request, 'Aula registrada exitosamente.')

        elif action == 'editar_aula':
            aula_id = request.POST.get('id')
            aula = get_object_or_404(Aula, id=aula_id)
            aula.nombre = request.POST.get('nombre')
            aula.nivel = request.POST.get('nivel')
            aula.capacidad = request.POST.get('capacidad')
            profesor_id = request.POST.get('profesor')
            aula.profesor = Profesor.objects.get(id=profesor_id)
            aula.save()
            messages.success(request, 'Aula editada exitosamente.')

        elif action == 'eliminar_aula':
            aula_id = request.POST.get('id')
            aula = get_object_or_404(Aula, id=aula_id)
            aula.delete()
            messages.success(request, 'Aula eliminada exitosamente.')

        # Acciones para comentarios
        elif action == 'agregar_comentario':
            texto = request.POST.get('texto')
            evaluacion_id = request.POST.get('evaluacion_id')
            profesor_id = request.POST.get('profesor_id')
            evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
            profesor = get_object_or_404(Profesor, id=profesor_id)
            Comentario.objects.create(texto=texto, evaluacion=evaluacion, profesor=profesor)
            messages.success(request, 'Comentario agregado exitosamente.')

        elif action == 'editar_comentario':
            comentario_id = request.POST.get('id')
            comentario = get_object_or_404(Comentario, id=comentario_id)
            comentario.texto = request.POST.get('texto')
            comentario.save()
            messages.success(request, 'Comentario editado exitosamente.')

        elif action == 'eliminar_comentario':
            comentario_id = request.POST.get('id')
            comentario = get_object_or_404(Comentario, id=comentario_id)
            comentario.delete()
            messages.success(request, 'Comentario eliminado exitosamente.')

        return redirect('panel_director')
    
     # Obtener todos los comentarios (tanto de evaluaciones como de estudiantes)
    comentarios_evaluaciones = Comentario.objects.filter(evaluacion__isnull=False)  # Comentarios sobre evaluaciones
    comentarios_estudiantes = Comentario.objects.filter(estudiante__isnull=False)    # Comentarios sobre estudiantes

    # Combinar ambos tipos de comentarios en una sola lista
    comentarios = list(comentarios_evaluaciones) + list(comentarios_estudiantes)

    context = {
        'aulas': aulas,
        'evaluaciones': evaluaciones,
        'eventos': eventos,
        'profesores': profesores,
        'comentarios': comentarios,  # Pasamos todos los comentarios al contexto
    }
    return render(request, 'panel-director.html', context)

def panel_profesor(request):
    # Obtener el ID del profesor de la sesión
    profesor_id = request.session.get('profesor_id')
    if not profesor_id:
        return redirect('profesor_login')

    # Obtener el objeto Profesor
    try:
        profesor = Profesor.objects.get(id=profesor_id)
    except Profesor.DoesNotExist:
        messages.error(request, 'Profesor no encontrado. Por favor, inicie sesión nuevamente.')
        return redirect('profesor_login')

    # Obtener los estudiantes del aula del profesor
    aula = Aula.objects.filter(profesor=profesor).first()
    estudiantes = Estudiante.objects.filter(aula=aula) if aula else []

    # Obtener las evaluaciones del aula
    evaluaciones = Evaluacion.objects.filter(aula=aula) if aula else []

    # Obtener los eventos (notificaciones)
    eventos = Evento.objects.all()

    # Obtener los comentarios del profesor
    comentarios_evaluaciones = Comentario.objects.filter(profesor=profesor, evaluacion__isnull=False)
    comentarios_estudiantes = Comentario.objects.filter(profesor=profesor, estudiante__isnull=False)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'agregar_comentario':
            texto = request.POST.get('texto')
            evaluacion_id = request.POST.get('evaluacion_id', None)  # Puede ser None si no se envía
            estudiante_id = request.POST.get('estudiante_id', None)  # Puede ser None si no se envía

            if evaluacion_id:
                # Si se envía evaluacion_id, es un comentario sobre una evaluación
                try:
                    evaluacion = Evaluacion.objects.get(id=evaluacion_id)
                    Comentario.objects.create(texto=texto, evaluacion=evaluacion, profesor=profesor)
                    messages.success(request, 'Comentario sobre evaluación agregado exitosamente.')
                except Evaluacion.DoesNotExist:
                    messages.error(request, 'Evaluación no encontrada.')
            elif estudiante_id:
                # Si se envía estudiante_id, es un comentario sobre un estudiante
                try:
                    estudiante = Estudiante.objects.get(id=estudiante_id)
                    Comentario.objects.create(texto=texto, estudiante=estudiante, profesor=profesor)
                    messages.success(request, 'Comentario sobre estudiante agregado exitosamente.')
                except Estudiante.DoesNotExist:
                    messages.error(request, 'Estudiante no encontrado.')
            else:
                messages.error(request, 'Debes seleccionar una evaluación o un estudiante.')

            return redirect('panel_profesor')

        elif action == 'editar_comentario':
            comentario_id = request.POST.get('id')
            comentario = get_object_or_404(Comentario, id=comentario_id)
            comentario.texto = request.POST.get('texto')
            comentario.save()
            messages.success(request, 'Comentario editado exitosamente.')
            return redirect('panel_profesor')

        elif action == 'eliminar_comentario':
            comentario_id = request.POST.get('id')
            comentario = get_object_or_404(Comentario, id=comentario_id)
            comentario.delete()
            messages.success(request, 'Comentario eliminado exitosamente.')
            return redirect('panel_profesor')

    context = {
        'profesor': profesor,
        'estudiantes': estudiantes,
        'evaluaciones': evaluaciones,
        'eventos': eventos,
        'comentarios_evaluaciones': comentarios_evaluaciones,
        'comentarios_estudiantes': comentarios_estudiantes,
    }
    return render(request, 'panel-profesor.html', context)



# API Views
@require_http_methods(["GET"])
def estudiantes_por_aula_api(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    estudiantes = aula.get_estudiantes()
    data = [{
        'id': e.id, 
        'nombre': e.nombre,
        'edad': e.edad
        } for e in estudiantes]
    return JsonResponse(data, safe=False)

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
    # Eliminar esta vista ya que la tabla Clase ha sido eliminada
    pass

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
    # Eliminar esta vista ya que la tabla Clase ha sido eliminada
    pass

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