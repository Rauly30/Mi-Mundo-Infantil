import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escuela.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Crear grupos
profesores_group, created = Group.objects.get_or_create(name='Profesores')
directores_group, created = Group.objects.get_or_create(name='Directores')

# Crear usuario profesor
profesor_user, created = User.objects.get_or_create(username='profesor')
if created:
    profesor_user.set_password('contraseña_profesor')  # Reemplaza 'contraseña_profesor' con la contraseña deseada
    profesor_user.save()
    profesores_group.user_set.add(profesor_user)
else:
    print("El usuario 'profesor' ya existe.")

# Crear usuario director
director_user, created = User.objects.get_or_create(username='director')
if created:
    director_user.set_password('contraseña_director')  # Reemplaza 'contraseña_director' con la contraseña deseada
    director_user.save()
    directores_group.user_set.add(director_user)
else:
    print("El usuario 'director' ya existe.")

print("Usuarios y grupos creados correctamente.")
