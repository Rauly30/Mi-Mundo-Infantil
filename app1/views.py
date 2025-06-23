from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import Profesor, Director, Estudiante, Aula, Evaluacion, Evento, Comentario, Formulario, Representante, Boletin
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import json
from .models import Profesor, Director, Estudiante, Aula, Evaluacion, Evento, Comentario, Formulario

def index(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        descripcion = request.POST.get('descripcion')

        # Debugging: Print the received data
        print(f"Received data: nombre={nombre}, email={email}, telefono={telefono}, descripcion={descripcion}")

        try:
            Formulario.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                descripcion=descripcion
            )
            messages.success(request, 'Formulario enviado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al enviar el formulario: {e}')
            # Debugging: Print the exception
            print(f"Error: {e}")

        return redirect('index')

    return render(request, 'index.html')

# Vistas de login para los paneles

def director_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            director = Director.objects.get(email=email)
            # Verificar si el director está bloqueado
            if director.bloqueado:
                messages.error(request, 'Este usuario está bloqueado. Contacte al administrador.')
                return redirect('director_login')
            # Verificar la contraseña
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
            # Verificar si el profesor está bloqueado
            if profesor.bloqueado:
                messages.error(request, 'Este usuario está bloqueado. Contacte al administrador.')
                return redirect('profesor_login')
            # Verificar la contraseña
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
    # Verificar si el director está autenticado
    director_id = request.session.get('director_id')
    if not director_id:
        messages.error(request, 'Por favor, inicie sesión para acceder al panel.')
        return redirect('panel_director')

    # Obtener el objeto Director
    try:
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        messages.error(request, 'Director no encontrado. Por favor, inicie sesión nuevamente.')
        return redirect('panel_director')
    
    # Obtener todos los datos para mostrar en el template
    estudiantes = Estudiante.objects.all()
    aulas = Aula.objects.all()
    profesores = Profesor.objects.all()
    directores = Director.objects.all()
    # administradores = Administrador.objects.all()  # Elimina esta línea

    # Manejar las acciones CRUD
    if request.method == 'POST':
        action = request.POST.get('action')
        model_type = request.POST.get('model_type')

        if model_type == 'estudiante':
            if action == 'crear':
                # Crear un nuevo estudiante
                aula_id = request.POST.get('aula')
                aula = Aula.objects.get(id=aula_id) if aula_id else None

                # Verificar si el aula ha alcanzado su capacidad máxima
                if aula and aula.estudiantes.count() >= aula.capacidad:  # Use the correct related name
                    messages.error(request, f'El aula "{aula.nombre}" ha alcanzado su capacidad máxima.')
                else:
                    nombre = request.POST.get('nombre')
                    edad = request.POST.get('edad')
                    nivel = request.POST.get('nivel')
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
                estudiante.aula = get_object_or_404(Aula, id=aula_id) if aula_id else None

                # Verificar si el aula ha alcanzado su capacidad máxima antes de guardar
                if estudiante.aula and estudiante.aula.estudiantes.count() >= estudiante.aula.capacidad:
                    messages.error(request, f'El aula "{estudiante.aula.nombre}" ha alcanzado su capacidad máxima.')
                else:
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
                # Verificar si el correo ya está en uso
                email = request.POST.get('email')
                if Profesor.objects.filter(email=email).exists():
                    messages.error(request, 'El correo electrónico ya está en uso.')
                else:
                    # Crear un nuevo profesor
                    nombre = request.POST.get('nombre')
                    especialidad = request.POST.get('especialidad')
                    password = make_password(request.POST.get('password'))
                    Profesor.objects.create(nombre=nombre, especialidad=especialidad, email=email, password=password)
                    messages.success(request, 'Profesor agregado exitosamente.')
            elif action == 'editar':
                # Editar un profesor existente
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                email = request.POST.get('email')
                if Profesor.objects.filter(email=email).exclude(id=profesor_id).exists():
                    messages.error(request, 'El correo electrónico ya está en uso.')
                else:
                    profesor.nombre = request.POST.get('nombre')
                    profesor.especialidad = request.POST.get('especialidad')
                    profesor.email = email
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
            elif action == 'bloquear':
                # Bloquear un profesor
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                profesor.bloqueado = True
                profesor.save()
                messages.success(request, 'Profesor bloqueado exitosamente.')
            elif action == 'desbloquear':
                # Desbloquear un profesor
                profesor_id = request.POST.get('id')
                profesor = get_object_or_404(Profesor, id=profesor_id)
                profesor.bloqueado = False
                profesor.save()
                messages.success(request, 'Profesor desbloqueado exitosamente.')

        elif model_type == 'director':
            if action == 'crear':
                # Verificar si el correo ya está en uso
                email = request.POST.get('email')
                if Director.objects.filter(email=email).exists():
                    messages.error(request, 'El correo electrónico ya está en uso.')
                else:
                    # Crear un nuevo director
                    nombre = request.POST.get('nombre')
                    password = make_password(request.POST.get('password'))
                    Director.objects.create(nombre=nombre, email=email, password=password)
                    messages.success(request, 'Director agregado exitosamente.')
            elif action == 'editar':
                # Editar un director existente
                director_id = request.POST.get('id')
                director = get_object_or_404(Director, id=director_id)
                email = request.POST.get('email')
                if Director.objects.filter(email=email).exclude(id=director_id).exists():
                    messages.error(request, 'El correo electrónico ya está en uso.')
                else:
                    director.nombre = request.POST.get('nombre')
                    director.email = email
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
            elif action == 'bloquear':
                # Bloquear un director
                director_id = request.POST.get('id')
                director = get_object_or_404(Director, id=director_id)
                director.bloqueado = True
                director.save()
                messages.success(request, 'Director bloqueado exitosamente.')
            elif action == 'desbloquear':
                # Desbloquear un director
                director_id = request.POST.get('id')
                director = get_object_or_404(Director, id=director_id)
                director.bloqueado = False
                director.save()
                messages.success(request, 'Director desbloqueado exitosamente.')

        # Redirigir para evitar reenvíos del formulario
        return redirect('panel_administrador')

    # Renderizar el template con los datos
    context = {
        'director': director,
        'estudiantes': estudiantes,
        'aulas': aulas,
        'profesores': profesores,
        'directores': directores,
        # 'administradores': administradores,  # Elimina esta línea
    }
    return render(request, 'panel-administrador.html', context)

def panel_director(request):
    # Verificar si el director está autenticado
    director_id = request.session.get('director_id')
    if not director_id:
        messages.error(request, 'Por favor, inicie sesión para acceder al panel.')
        return redirect('director_login')

    # Obtener el objeto Director
    try:
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        messages.error(request, 'Director no encontrado. Por favor, inicie sesión nuevamente.')
        return redirect('director_login')
    
    aulas = Aula.objects.all()
    evaluaciones = Evaluacion.objects.all()
    eventos = Evento.objects.all()
    profesores = Profesor.objects.all()
    estudiantes = Estudiante.objects.all()
    representantes = Representante.objects.all()
    
    # Obtener todos los comentarios (tanto de evaluaciones como de estudiantes)
    comentarios_evaluaciones = Comentario.objects.filter(evaluacion__isnull=False)
    comentarios_estudiantes = Comentario.objects.filter(estudiante__isnull=False)
    comentarios = list(comentarios_evaluaciones) + list(comentarios_estudiantes)

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
            apellido = request.POST.get('apellido')
            especialidad = request.POST.get('especialidad')
            email = request.POST.get('email')
            password = make_password(request.POST.get('password'))
            Profesor.objects.create(nombre=nombre, apellido=apellido, especialidad=especialidad, email=email, password=password)
            messages.success(request, 'Profesor agregado exitosamente.')

        elif action == 'editar_profesor':
            profesor_id = request.POST.get('id')
            profesor = get_object_or_404(Profesor, id=profesor_id)
            profesor.nombre = request.POST.get('nombre')
            profesor.apellido = request.POST.get('apellido')
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

        elif action == 'bloquear_profesor':
            profesor_id = request.POST.get('id')
            profesor = get_object_or_404(Profesor, id=profesor_id)
            profesor.bloqueado = True
            profesor.save()
            messages.success(request, 'Profesor bloqueado exitosamente.')

        elif action == 'desbloquear_profesor':
            profesor_id = request.POST.get('id')
            profesor = get_object_or_404(Profesor, id=profesor_id)
            profesor.bloqueado = False
            profesor.save()
            messages.success(request, 'Profesor desbloqueado exitosamente.')

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

        elif action == 'registrar_estudiante':
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            nivel = request.POST.get('nivel')
            aula_id = request.POST.get('aula')
            aula = Aula.objects.get(id=aula_id)
            
            # Calcular edad
            hoy = date.today()
            fecha_nac = date.fromisoformat(fecha_nacimiento)
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            
            # Datos del representante
            cedula_representante = request.POST.get('cedula_representante')
            nombre_representante = request.POST.get('nombre_representante')
            apellido_representante = request.POST.get('apellido_representante')
            telefono_representante = request.POST.get('telefono_representante')
            email_representante = request.POST.get('email_representante')
            
            # Crear o actualizar representante
            representante, created = Representante.objects.get_or_create(
                cedula=cedula_representante,
                defaults={
                    'nombre': nombre_representante,
                    'apellido': apellido_representante,
                    'telefono': telefono_representante,
                    'email': email_representante
                }
            )
            
            # Crear estudiante
            Estudiante.objects.create(
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                edad=edad,
                nivel=nivel,
                aula=aula,
                representante=representante
            )
            messages.success(request, 'Estudiante registrado exitosamente.')

        elif action == 'editar_estudiante':
            estudiante_id = request.POST.get('id')
            estudiante = get_object_or_404(Estudiante, id=estudiante_id)
            estudiante.nombre = request.POST.get('nombre')
            estudiante.apellido = request.POST.get('apellido')
            estudiante.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            estudiante.nivel = request.POST.get('nivel')
            aula_id = request.POST.get('aula')
            estudiante.aula = Aula.objects.get(id=aula_id)
            
            # Calcular edad
            hoy = date.today()
            fecha_nac = date.fromisoformat(estudiante.fecha_nacimiento)
            estudiante.edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            
            representante_id = request.POST.get('representante')
            estudiante.representante = Representante.objects.get(id=representante_id)
            
            estudiante.save()
            messages.success(request, 'Estudiante editado exitosamente.')

        elif action == 'eliminar_estudiante':
            estudiante_id = request.POST.get('id')
            estudiante = get_object_or_404(Estudiante, id=estudiante_id)
            estudiante.delete()
            messages.success(request, 'Estudiante eliminado exitosamente.')

        elif action == 'editar_representante':
            representante_id = request.POST.get('id')
            representante = get_object_or_404(Representante, id=representante_id)
            representante.cedula = request.POST.get('cedula')
            representante.nombre = request.POST.get('nombre')
            representante.apellido = request.POST.get('apellido')
            representante.telefono = request.POST.get('telefono')
            representante.email = request.POST.get('email')
            representante.save()
            messages.success(request, 'Representante editado exitosamente.')

        elif action == 'eliminar_representante':
            representante_id = request.POST.get('id')
            representante = get_object_or_404(Representante, id=representante_id)
            representante.delete()
            messages.success(request, 'Representante eliminado exitosamente.')

        elif action == 'editar_director':
            director_id = request.POST.get('id')
            director = get_object_or_404(Director, id=director_id)
            director.nombre = request.POST.get('nombre')
            director.apellido = request.POST.get('apellido')
            director.email = request.POST.get('email')

            # Verificar si las contraseñas coinciden
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password:
                if password != confirm_password:
                    messages.error(request, 'Las contraseñas no coinciden.')
                    return redirect('panel_director')
                director.password = make_password(password)

            director.save()
            messages.success(request, 'Perfil actualizado exitosamente.')

        return redirect('panel_director')

    context = {
        'director': director,
        'aulas': aulas,
        'evaluaciones': evaluaciones,
        'eventos': eventos,
        'profesores': profesores,
        'estudiantes': estudiantes,
        'representantes': representantes,
        'comentarios': comentarios,
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

    # Obtener los boletines creados por el profesor
    boletines = Boletin.objects.filter(profesor=profesor)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'agregar_comentario':
            texto = request.POST.get('texto')
            evaluacion_id = request.POST.get('evaluacion_id', None)
            estudiante_id = request.POST.get('estudiante_id', None)

            if evaluacion_id:
                try:
                    evaluacion = Evaluacion.objects.get(id=evaluacion_id)
                    Comentario.objects.create(texto=texto, evaluacion=evaluacion, profesor=profesor)
                    messages.success(request, 'Comentario sobre evaluación agregado exitosamente.')
                except Evaluacion.DoesNotExist:
                    messages.error(request, 'Evaluación no encontrada.')
            elif estudiante_id:
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

        elif action == 'agregar_boletin':
            estudiante_id = request.POST.get('estudiante_id')
            periodo = request.POST.get('periodo')
            asignatura = request.POST.get('asignatura')
            calificacion = request.POST.get('calificacion')
            observaciones = request.POST.get('observaciones')
            
            estudiante = get_object_or_404(Estudiante, id=estudiante_id)
            
            Boletin.objects.create(
                estudiante=estudiante,
                periodo=periodo,
                asignatura=asignatura,
                calificacion=calificacion,
                observaciones=observaciones,
                profesor=profesor
            )
            messages.success(request, 'Boletín agregado exitosamente.')
            return redirect('panel_profesor')

        elif action == 'editar_boletin':
            boletin_id = request.POST.get('id')
            boletin = get_object_or_404(Boletin, id=boletin_id)
            boletin.estudiante_id = request.POST.get('estudiante_id')
            boletin.periodo = request.POST.get('periodo')
            boletin.asignatura = request.POST.get('asignatura')
            boletin.calificacion = request.POST.get('calificacion')
            boletin.observaciones = request.POST.get('observaciones')
            boletin.save()
            messages.success(request, 'Boletín editado exitosamente.')
            return redirect('panel_profesor')

        elif action == 'eliminar_boletin':
            boletin_id = request.POST.get('id')
            boletin = get_object_or_404(Boletin, id=boletin_id)
            boletin.delete()
            messages.success(request, 'Boletín eliminado exitosamente.')
            return redirect('panel_profesor')

        elif action == 'editar_profesor':
            profesor_id = request.POST.get('id')
            profesor = get_object_or_404(Profesor, id=profesor_id)
            profesor.nombre = request.POST.get('nombre')
            profesor.apellido = request.POST.get('apellido')
            profesor.email = request.POST.get('email')

            # Verificar si las contraseñas coinciden
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password:
                if password != confirm_password:
                    messages.error(request, 'Las contraseñas no coinciden.')
                    return redirect('panel_profesor')
                profesor.password = make_password(password)

            profesor.save()
            messages.success(request, 'Perfil actualizado exitosamente.')

    context = {
        'profesor': profesor,
        'estudiantes': estudiantes,
        'evaluaciones': evaluaciones,
        'eventos': eventos,
        'comentarios_evaluaciones': comentarios_evaluaciones,
        'comentarios_estudiantes': comentarios_estudiantes,
        'boletines': boletines,
    }
    return render(request, 'panel-profesor.html', context)

def panel_representante(request):
    estudiante = None
    representante = None
    boletines = []
    comentarios = []
    
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        nombre_completo = request.POST.get('nombre_estudiante', '').strip().upper()  # Convertir a mayúsculas
        
        if not cedula or not nombre_completo:
            messages.error(request, 'Por favor complete todos los campos.')
        else:
            try:
                # Limpiar la cédula (solo números)
                cedula_limpia = ''.join(c for c in cedula if c.isdigit())
                
                # Buscar representante por cédula exacta
                representante = Representante.objects.get(cedula=cedula_limpia)
                
                # Obtener todos los estudiantes del representante
                estudiantes = representante.estudiantes.all()
                
                # Filtrar estudiantes por nombre completo (nombre + apellido)
                estudiantes_filtrados = [
                    e for e in estudiantes 
                    if nombre_completo in f"{e.nombre} {e.apellido}".upper()
                ]
                
                if estudiantes_filtrados:
                    estudiante = estudiantes_filtrados[0]  # Tomar el primer estudiante que coincida
                    
                    # Obtener boletines y comentarios
                    boletines = Boletin.objects.filter(
                        estudiante=estudiante
                    ).select_related('profesor').order_by('-fecha')
                    
                    comentarios = Comentario.objects.filter(
                        estudiante=estudiante
                    ).select_related('profesor').order_by('-fecha')
                else:
                    # Mensaje más informativo con los estudiantes disponibles
                    nombres_estudiantes = [f"{e.nombre} {e.apellido}" for e in estudiantes]
                    messages.error(
                        request, 
                        f'No se encontró un estudiante que coincida con "{nombre_completo}". '
                        f'Estudiantes asociados a esta cédula: {", ".join(nombres_estudiantes) or "Ninguno"}'
                    )
                    
            except Representante.DoesNotExist:
                messages.error(request, f'No existe un representante con cédula {cedula}')
            except Exception as e:
                messages.error(request, f'Error en la búsqueda: {str(e)}')
                # Registrar el error para diagnóstico
                import logging
                logging.error(f"Error en panel_representante: {str(e)}")
    
    context = {
        'estudiante': estudiante,
        'representante': representante,
        'boletines': boletines,
        'comentarios': comentarios,
        'search_performed': request.method == 'POST'
    }
    return render(request, 'representante.html', context)

@require_http_methods(["GET"])
def get_estudiantes(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    estudiantes = Estudiante.objects.filter(aula=aula)
    estudiantes_data = [{
        "nombre": estudiante.nombre,
        "apellido": estudiante.apellido,
        "edad": estudiante.edad,
        "representante": f"{estudiante.representante.nombre} {estudiante.representante.apellido}"
    } for estudiante in estudiantes]
    return JsonResponse(estudiantes_data, safe=False)

def logout(request):
    request.session.flush()
    return redirect('index')