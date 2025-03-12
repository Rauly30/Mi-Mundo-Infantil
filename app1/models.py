from django.db import models
from django.utils import timezone

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Director(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    nivel = models.CharField(max_length=20)
    aula = models.ForeignKey('Aula', on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')

    def __str__(self):
        return self.nombre

class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20)
    capacidad = models.PositiveIntegerField()
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='aulas')

    def __str__(self):
        return self.nombre

    def get_estudiantes(self):
        return self.estudiantes.all()

class Evaluacion(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='evaluaciones', default=1)
    plan = models.TextField()

    def __str__(self):
        return f"Evaluación de {self.aula.nombre}"

class Evento(models.Model):
    fecha = models.DateField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)

    def __str__(self):
        return f"Comentario: {self.texto[:50]}..."