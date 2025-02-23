from django.db import models

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)  # Agregado campo de nombre
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Custom model for Clients
class Director(models.Model):
    nombre = models.CharField(max_length=100)  # Agregado campo de nombre
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Custom model for Clients
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)  # Agregado campo de nombre
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre