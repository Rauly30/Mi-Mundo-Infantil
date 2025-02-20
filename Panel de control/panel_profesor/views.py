from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

def is_profesor(user):
    return user.groups.filter(name='Profesores').exists()

@login_required
@user_passes_test(is_profesor)
def panel_profesor(request):
    return render(request, 'panel-profesor.html')
