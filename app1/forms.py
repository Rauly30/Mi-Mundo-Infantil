from django import forms
from .models import Estudiante, Aula, Profesor, Acceso

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'edad', 'nivel', 'aula']