from django.db import models
from django.utils import timezone

class Representante(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Director(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20)
    capacidad = models.PositiveIntegerField()
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='aulas')

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    edad = models.PositiveIntegerField()
    nivel = models.CharField(max_length=20)
    aula = models.ForeignKey(Aula, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    representante = models.ForeignKey(Representante, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

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

class Boletin(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='boletines')
    periodo = models.CharField(max_length=50)
    asignatura = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2)
    observaciones = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='boletines')

    def __str__(self):
        return f"Boletín de {self.estudiante} - {self.periodo}"

class Comentario(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)

    def __str__(self):
        return f"Comentario: {self.texto[:50]}..."

class Formulario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre